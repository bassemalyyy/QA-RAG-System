import streamlit as st
import time
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import DEFAULT_SYSTEM_MESSAGE

def configure_page():
    st.set_page_config(
        page_title="Document QA RAG",
        page_icon="📄",
        layout="centered",
    )
    st.title("Document QA RAG Assistant")
    st.markdown("### Chat with Your Documents using AI")


def center_app():
    st.markdown(
        """
        <style>
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 800px;
            margin: auto;
        }
        .stTextInput, .stButton {
            width: 100% !important;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def handle_new_document_button():
    if st.sidebar.button("🔄 New Document", use_container_width=True):
        if "retriever" in st.session_state:
            del st.session_state["retriever"]
        if "document_name" in st.session_state:
            del st.session_state["document_name"]

        st.session_state.messages = [SystemMessage(content=DEFAULT_SYSTEM_MESSAGE)]
        st.success("🔄 Ready for new document!")
        time.sleep(1)
        st.rerun()