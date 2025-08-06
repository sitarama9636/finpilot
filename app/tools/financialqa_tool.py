from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

# 🧠 Step 1: Setup the vector retriever
def get_vector_retriever(persist_directory="chroma_vectordb") -> VectorStoreRetriever:
    embedding_function = HuggingFaceEmbeddings(
        model_name="intfloat/e5-small-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        cache_folder="models"
    )
    vectorstore = Chroma(
        collection_name="rag_collection",
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    return vectorstore.as_retriever()

# 🛠️ Step 2: Define the tool
@tool
def answer_financial_question(query: str) -> str:
    """Answer financial questions using retrieved company documents."""
    print(f"[🔍] Financial question: {query}")

    llm = Ollama(model="llama3.2")
    retriever = get_vector_retriever()

    docs: list[Document] = retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant financial information found. Please upload documents."

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""Use the context below to answer the financial question.

Context:
{context}

Question:
{query}

Answer in a concise and factual manner:"""

    return llm.invoke(prompt)
