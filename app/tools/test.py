# test_pdf_tool.py

from app.tools import pdfretriver_tool

if __name__ == "__main__":
    query = "What is prince?"
    answer = pdfretriver_tool.pdf_qa_tool(query)
    print("\n📄 Answer:\n", answer)
