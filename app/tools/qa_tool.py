# tools/qa_tool.py

from langchain_core.tools import tool
from app.tools.pdfretriver_tool import pdf_qa_tool

@tool
def answer_pdf_question(query: str) -> str:
    """Answer user queries based on uploaded PDF documents."""
    return pdf_qa_tool(query)
