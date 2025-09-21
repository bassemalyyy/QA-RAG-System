import os
import tempfile
import time
import streamlit as st
import logging
from streamlit.runtime.uploaded_file_manager import UploadedFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_docling.loader import DoclingLoader
from huggingface_hub import login as hf_login
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, RETRIEVER_K

logger = logging.getLogger(__name__)

def handle_document_processing(uploaded_file: UploadedFile | None = None):
    """
    Process an uploaded document with logging and error handling.
    """
    if st.button("🚀 Process Document", type="primary"):
        user_api_key = st.session_state.get("api_key", "")
        if not user_api_key:
            st.error("❌ Please enter your Google Gemini API key in the sidebar first!")
            logger.warning("Attempted to process document but Google Gemini API key is missing.")
            return

        if not uploaded_file:
            st.error("❌ Please upload a document first!")
            logger.warning("Attempted to process document but no file was uploaded.")
            return

        with st.spinner("Processing document..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            tmp_file_path = None  

            try:
                # --- Step 1: Save to temp ---
                status_text.text("🔄 Step 1/6: Saving document to a temporary file...")
                progress_bar.progress(10)
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                logger.info("Saved uploaded file to temp: %s", tmp_file_path)

                # --- Step 2: Loader ---
                status_text.text("📄 Step 2/6: Preparing loader...")
                progress_bar.progress(25)

                if uploaded_file.name.lower().endswith(".pdf"):
                    huggingface_api_key = (
                        st.session_state.get("huggingface_api_key", "")
                        or os.getenv("HUGGINGFACEHUB_API_TOKEN")
                    )
                    if not huggingface_api_key:
                        st.error("❌ Please enter your Hugging Face API key in the sidebar first!")
                        logger.warning("Hugging Face API key missing; cannot use DoclingLoader for PDF.")
                        os.unlink(tmp_file_path)
                        return
                    hf_login(token=huggingface_api_key)
                    logger.info("Logged into Hugging Face Hub successfully.")
                    loader = DoclingLoader(tmp_file_path)
                    logger.info("DoclingLoader initialized for PDF.")
                else:
                    loader = TextLoader(tmp_file_path)
                    logger.info("TextLoader initialized for text file.")

                # --- Step 3: Load ---
                status_text.text("📥 Step 3/6: Loading document into memory...")
                progress_bar.progress(40)
                documents = loader.load()
                logger.info("Document loaded: %s documents returned.", len(documents) if documents else 0)

                if not documents:
                    st.error("❌ No text could be extracted from the document. Please upload a valid file.")
                    logger.error("No text extracted from file: %s", uploaded_file.name)
                    os.unlink(tmp_file_path)
                    return

                # --- Step 4: Split ---
                status_text.text("✂️ Step 4/6: Splitting into chunks...")
                progress_bar.progress(60)
                splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                chunks = splitter.split_documents(documents)
                logger.info("Document split into chunks: %d chunks.", len(chunks))

                if not chunks:
                    st.error("❌ Document could not be split into chunks (empty content).")
                    logger.error("No chunks created for file: %s", uploaded_file.name)
                    os.unlink(tmp_file_path)
                    return

                # --- Step 5: Embeddings ---
                status_text.text("🧠 Step 5/6: Creating embeddings...")
                progress_bar.progress(80)
                embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
                logger.info("Embedding model initialized: %s", EMBEDDING_MODEL)

                vector_store = FAISS.from_documents(chunks, embeddings)
                logger.info("FAISS vector store created (num_chunks=%d).", len(chunks))

                # --- Step 6: Retriever ---
                status_text.text("🔎 Step 6/6: Creating retriever and finalizing...")
                progress_bar.progress(95)
                retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": RETRIEVER_K})
                st.session_state["retriever"] = retriever
                st.session_state["document_name"] = uploaded_file.name
                logger.info("Retriever created (k=%d) and stored in session_state.", RETRIEVER_K)

                os.unlink(tmp_file_path)
                logger.info("Temporary file removed: %s", tmp_file_path)

                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                st.success("✅ Document processed! Ready for questions.")
                logger.info("Document processing completed successfully for file: %s", uploaded_file.name)
                time.sleep(1)
                st.rerun()

            except Exception as e:
                logger.exception("❌ Error processing document: %s", e)
                st.error(f"❌ Error processing document: {str(e)}")
                if tmp_file_path and os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    logger.info("Temporary file removed after exception: %s", tmp_file_path)