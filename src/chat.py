import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import format_docs

@st.cache_resource()
def get_chat_model(model_name: str, api_key_keyed_for_cache: str | None):
    return ChatGoogleGenerativeAI(model=model_name)

def display_chat_messages():
    for message in st.session_state.messages[1:]:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(message.content)

def handle_user_input(chat_model, input_disabled: bool = False):
    if prompt := st.chat_input("Ask a question about the document...", disabled=input_disabled):
        if not prompt.strip():
            st.warning("Please type a message before sending!")
            return

        st.session_state.messages.append(HumanMessage(content=prompt))
        prompt_template = PromptTemplate(
            template="Based on this document content:\n\n{context}\n\nQuestion: {question}",
            input_variables=["context", "question"],
        )

        with st.chat_message("user"):
            st.write(prompt)

        retriever = st.session_state.get("retriever")
        if not retriever:
            with st.chat_message("assistant"):
                error_msg = "❌ Please process a document first to enable question answering."
                st.error(error_msg)
                st.session_state.messages.append(AIMessage(content=error_msg))
            return

        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing document content..."):
                try:
                    retrieved_docs = retriever.invoke(prompt)
                    if not retrieved_docs:
                        no_context_msg = "🤷‍♂️ I couldn't find relevant info in the document."
                        st.warning(no_context_msg)
                        st.session_state.messages.append(AIMessage(content=no_context_msg))
                        return

                    parallel_chain = RunnableParallel({
                        "context": retriever | RunnableLambda(format_docs),
                        "question": RunnablePassthrough(),
                    })
                    parser = StrOutputParser()
                    main_chain = parallel_chain | prompt_template | chat_model | parser

                    message_placeholder = st.empty()
                    full_response = ""

                    for chunk in main_chain.stream(prompt):
                        if chunk and chunk.strip():
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")

                    if full_response.strip():
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append(AIMessage(content=full_response))
                    else:
                        error_msg = "🚫 No response received. Try a different model."
                        message_placeholder.error(error_msg)
                        st.session_state.messages.append(AIMessage(content=error_msg))

                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.messages.append(AIMessage(content=f"❌ Error: {str(e)}"))