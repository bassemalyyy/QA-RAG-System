import os
import streamlit as st
import logging
from state import init_session_state
from ui import configure_page, center_app, handle_new_document_button
from document_handler import handle_document_processing
from chat import get_chat_model, display_chat_messages, handle_user_input
from config import DEFAULT_SYSTEM_MESSAGE

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="w",   # overwrite log file on each run
    encoding="utf-8"
)
logger = logging.getLogger(__name__)

# --- Init session & UI ---
init_session_state()
configure_page()
center_app()

# --- Sidebar ---
selected_model = st.sidebar.selectbox(
    "Generation Model",
    ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.5-flash"],
    index=0
)
user_api_key = st.sidebar.text_input("Google Gemini API Key", type="password", placeholder="Enter your API key...")
huggingface_api_key = st.sidebar.text_input("Hugging Face API Key", type="password", placeholder="Enter your Hugging Face API key...")

if user_api_key:
    st.session_state.api_key = user_api_key
    os.environ["GOOGLE_API_KEY"] = user_api_key
    logger.info("Google Gemini API key has been set.")
else:
    logger.warning("Google Gemini API key is not set.")

if huggingface_api_key:
    st.session_state.huggingface_api_key = huggingface_api_key
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_api_key
    logger.info("Hugging Face API key has been set.")
else:
    logger.warning("Hugging Face API key is not set.")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your document", type=["pdf", "txt"])
if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    st.info(f"📊 Size: {uploaded_file.size} bytes")
    logger.info(f"File uploaded: {uploaded_file.name}, Size: {uploaded_file.size} bytes")

    try:
        logger.info("🚀 Starting document processing...")
        handle_document_processing(uploaded_file)
        logger.info("✅ Document processing completed successfully.")
    except Exception as e:
        logger.error(f"❌ Error processing document: {str(e)}", exc_info=True)

# --- Chat Section ---
chat_model = get_chat_model(selected_model, user_api_key) if user_api_key else None

display_chat_messages()
if chat_model is None:
    st.warning("Please enter your Google Gemini API key to start chatting.")
    logger.warning("Chat model is not initialized because the API key is missing.")
else:
    logger.info("✅ Chat model initialized successfully.")

handle_user_input(chat_model, input_disabled=(chat_model is None))
