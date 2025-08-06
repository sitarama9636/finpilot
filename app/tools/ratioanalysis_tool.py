# app/tools/ratioanalysis_tool.py

from langchain_core.tools import tool
from langchain_core.language_models import BaseLanguageModel
from langchain_core.documents import Document
from typing import List

# These will be set when initializing the tool externally
llm: BaseLanguageModel = None
retriever = None

@tool
def ratio_analysis(query: str) -> str:
    """Perform financial ratio analysis using retrieved financial data."""
    print(f"[📊] Performing ratio analysis for: {query}")
    docs: List[Document] = retriever.get_relevant_documents(query)

    if not docs:
        return "❌ No relevant financial data found to perform ratio analysis."

    context = "\n".join(doc.page_content for doc in docs[:4])  # Use top 4 docs
    prompt = (
        f"Based on the following financial data, extract and explain key financial ratios "
        f"(e.g., liquidity, profitability, debt-equity, etc.):\n\n{context}\n\nAnswer:"
    )
    return llm.invoke(prompt)
