# app/tools/test_ratio.py

from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.tools import ratioanalysis_tool  # Import the module, not the function

# Set up LLM
llm = Ollama(model="llama3.2")

# Set up embeddings
embedding_function = HuggingFaceEmbeddings(
    model_name="intfloat/e5-small-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
    cache_folder="models"
)

# Set up retriever
retriever = Chroma(
    collection_name="rag_collection",
    persist_directory="chroma_vectordb",
    embedding_function=embedding_function
).as_retriever()

# Inject dependencies into the tool module
ratioanalysis_tool.llm = llm
ratioanalysis_tool.retriever = retriever

# Call the tool
query = "What are the liquidity and profitability ratios for NVIDIA for Q1 2024?"
response = ratioanalysis_tool.ratio_analysis.invoke(query)

print(response)
