from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import torch
from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/e5-small-v2")

def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": DEVICE},
        encode_kwargs={"normalize_embeddings": True},
        cache_folder="models"
    )
    return embeddings
