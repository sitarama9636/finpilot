from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def get_vector_retriever(persist_directory="chroma_vectordb"):
    embedding_function = HuggingFaceEmbeddings(
        model_name="intfloat/e5-small-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        cache_folder="models"
    )

    db = Chroma(
        collection_name="rag_collection",
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    
    return db.as_retriever()
