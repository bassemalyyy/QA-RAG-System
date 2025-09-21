# Format retrieved documents into a string
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)