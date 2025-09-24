📘 RAG Q&A System
=================

A **Retrieval-Augmented Generation (RAG)** powered **Q&A system** built with **Streamlit**, **FAISS**, and **Google Generative AI embeddings**.\
This project allows you to upload documents (PDF or TXT), automatically process them into vector embeddings, and interact with them through an intelligent retriever for **question answering**.

The system uses **document loaders (Docling/TextLoader)** to handle different file formats, **recursive chunking** for splitting large documents, and **FAISS** for efficient similarity search. By combining these with **Google Generative AI embeddings**, it creates a powerful local knowledge base you can query in natural language.

🌐 Live Demo
----------

[Give it a try here!](https://docs-rag-system.streamlit.app/)

✨ Features
----------

-   📂 Upload and process **PDF or TXT documents**

-   ✂️ **Chunking and embedding** with Google Generative AI

-   🔍 Store vectors in **FAISS** for fast retrieval

-   🤖 Query your documents using **retrieval-based Q&A**

-   🚀 Simple, interactive **Streamlit web interface**

📦 Tech Stack
-------------

-   [Streamlit](https://streamlit.io/) -- Web interface

-   [LangChain](https://www.langchain.com/) -- Document loaders, chunking, retriever

-   [FAISS](https://github.com/facebookresearch/faiss) -- Vector store for embeddings

-   [Google Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings) -- Embedding model

-   [Hugging Face](https://huggingface.co/) -- Used for gated model access in Docling

⚡ Installation
--------------

Clone the repo:
```bash
git clone https://github.com/bassemalyyy/QA-RAG-System.git
cd qa_rag_system
```

Create a virtual environment & install dependencies:

```bash
python -m venv myenv
source myenv/bin/activate  # (Linux/Mac)
myenv\Scripts\activate     # (Windows)

pip install -r requirements.txt
```

🔑 Environment Variables
------------------------

Create a `.env` file in the project root and add your API keys:
```bash
GOOGLE_API_KEY=your_google_gemini_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
```

▶️ Usage
--------

Run the Streamlit app:

`streamlit run app.py`

Steps inside the app:

1.  Enter your **Google API Key** (and Hugging Face token if using PDF loader).

2.  Upload a `.pdf` or `.txt` document.

3.  Click **🚀 Process Document**.

4.  Start asking questions in natural language.

🚧 Known Issues
---------------

-   Large PDFs may take longer to process.

-   Requires both **Google API Key** and **Hugging Face API Key** for full functionality.

🤝 Contributing
---------------

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📜 License
----------

This project is licensed under the **MIT License**.