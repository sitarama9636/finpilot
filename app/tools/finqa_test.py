from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.tools.financialqa_tool import FinancialQATool

# Load LLM
llm = Ollama(model="llama3.2")

# Create Retriever
embedding_function = HuggingFaceEmbeddings(
    model_name="intfloat/e5-small-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
    cache_folder="models"
)

retriever = Chroma(
    collection_name="rag_collection",
    persist_directory="chroma_vectordb",
    embedding_function=embedding_function
).as_retriever()

# Initialize QA tool
qa_tool = FinancialQATool(llm=llm, retriever=retriever)

# Ask a question
query = "What are the top financial highlights for NVIDIA in the first quarter of 2024?"
response = qa_tool.answer_financial_question.invoke({"query": query})

# Print result
print(response)
