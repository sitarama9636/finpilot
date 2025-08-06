from langchain.tools import tool
from langchain_core.language_models import BaseLanguageModel
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

import re


# Step 1: Initialize Chroma vector retriever
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


# Step 2: Extract companies using LLM instead of regex
def extract_companies_with_llm(llm: BaseLanguageModel, query: str) -> list[str]:
    prompt = (
        f"Extract exactly two company names from the following query:\n\n"
        f"{query}\n\n"
        f"Respond with just a comma-separated list of two companies, like:\n"
        f"CompanyA, CompanyB"
    )
    response = llm.invoke(prompt)
    companies = [c.strip() for c in response.split(",") if c.strip()]
    return companies[:2]


# Step 3: Validate if documents are meaningful
def is_valid_docs(docs: list[Document]) -> bool:
    return docs and sum(len(doc.page_content.strip()) > 100 for doc in docs) >= 2


# Step 4: Main Tool
class CompanyComparisonTool:
    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.retriever = get_vector_retriever()

    def compare(self, query: str) -> str:
        companies = extract_companies_with_llm(self.llm, query)
        if len(companies) < 2:
            return "❗ Please ask to compare exactly two companies."

        company1, company2 = companies
        print(f"[🔍] Comparing: {company1} vs {company2}")

        docs1 = self.retriever.get_relevant_documents(f"{company1} financials")
        docs2 = self.retriever.get_relevant_documents(f"{company2} financials")

        valid1 = is_valid_docs(docs1)
        valid2 = is_valid_docs(docs2)

        if not valid1 and not valid2:
            return (
                f"❌ I couldn't find relevant info for **{company1}** or **{company2}**.\n"
                "👉 Please upload documents, provide URLs, or paste text."
            )

        if valid1 and not valid2:
            summary1 = self._summarize_docs(company1, docs1)
            return (
                f"📊 Found info for **{company1}** only:\n\n{summary1}\n\n"
                f"❌ No data found for **{company2}**. Please upload or provide source."
            )

        if valid2 and not valid1:
            summary2 = self._summarize_docs(company2, docs2)
            return (
                f"📊 Found info for **{company2}** only:\n\n{summary2}\n\n"
                f"❌ No data found for **{company1}**. Please upload or provide source."
            )

        # Both are valid – do full comparison
        context1 = "\n".join([doc.page_content for doc in docs1[:4]])
        context2 = "\n".join([doc.page_content for doc in docs2[:4]])

        prompt = (
            f"Compare the financial and strategic information between:\n\n"
            f"🔹 {company1}:\n{context1}\n\n"
            f"🔹 {company2}:\n{context2}\n\n"
            "Please provide a detailed but concise comparison."
        )
        return self.llm.invoke(prompt)

    def _summarize_docs(self, company: str, docs: list[Document]) -> str:
        context = "\n".join([doc.page_content for doc in docs[:4]])
        prompt = (
            f"Summarize the financial highlights and strategies for {company}:\n\n"
            f"{context}\n\nSummary:"
        )
        return self.llm.invoke(prompt)


# Optional: Expose as @tool
@tool
def compare_companies(query: str) -> str:
    """Compare two companies' financials and strategies based on available documents."""
    llm = Ollama(model="llama3.2")  # Update your model name if needed
    tool = CompanyComparisonTool(llm)
    return tool.compare(query)
