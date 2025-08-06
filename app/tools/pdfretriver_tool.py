# tools/pdf_retriever_tool.py

from langchain.tools import tool
from app.tools import pdfretriever

# Initialize retriever once at module level
retriever = pdfretriever.get_vector_retriever()

@tool
def pdf_qa_tool(query: str) -> str:
    """
    Searches company documents and returns relevant information based on the user's query.
    """
    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "No relevant information found in company documents."
    
    return "\n\n".join(doc.page_content for doc in docs[:3])  # Return top 3 chunks
