import streamlit as st
from langchain_core.messages import SystemMessage
from config import DEFAULT_SYSTEM_MESSAGE

def init_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=DEFAULT_SYSTEM_MESSAGE)]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []