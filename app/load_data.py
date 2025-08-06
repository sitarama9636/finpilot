import os
import json
import shutil
import hashlib
from typing import List
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from chromadb import PersistentClient
from get_embedding_function import get_embedding_function

from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env

DEVICE = os.getenv("DEVICE", "cpu")
EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/e5-small-v2")


# Paths (can be overridden)
CHROMA_PATH = "chroma_vectordb"
HASH_RECORD_FILE = "pdf_hashes.json"


def load_documents(data_path="data") -> List[Document]:
    loader = PyPDFDirectoryLoader(data_path)
    all_docs = loader.load()

    current_hashes = _load_hashes()
    new_hashes = {}
    updated_docs = []

    for doc in all_docs:
        source = doc.metadata.get("source")
        file_path = os.path.join(data_path, os.path.basename(source))
        file_hash = _get_file_hash(file_path)

        new_hashes[source] = file_hash

        if current_hashes.get(source) != file_hash:
            updated_docs.append(doc)
        else:
            print(f"[⏩] Skipping unchanged: {source}")

    _save_hashes(new_hashes)
    print(f"[📄] Loaded {len(updated_docs)} updated documents.")
    return updated_docs


def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    chunks = [c for c in chunks if c.page_content.strip()]
    return chunks


def assign_chunk_ids(chunks: List[Document]) -> List[Document]:
    last_page_id = None
    chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown.pdf")
        page = chunk.metadata.get("page", "0")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            chunk_index += 1
        else:
            chunk_index = 0

        chunk_id = f"{current_page_id}:{chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks


def add_to_chroma(chunks: List[Document], chroma_path=CHROMA_PATH):
    if not chunks:
        print("🚫 No chunks to embed.")
        return

    embedding = get_embedding_function()
    texts = [c.page_content for c in chunks]
    metadatas = [c.metadata for c in chunks]
    ids = [m["id"] for m in metadatas]

    client = PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection("rag_collection")

    existing = collection.get(ids=ids)
    existing_ids = set(existing.get("ids", []))
    new_indices = [i for i, id_ in enumerate(ids) if id_ not in existing_ids]

    if not new_indices:
        print("✅ No new chunks to add.")
        return

    to_add = {
        "ids": [ids[i] for i in new_indices],
        "documents": [texts[i] for i in new_indices],
        "metadatas": [metadatas[i] for i in new_indices],
        "embeddings": embedding.embed_documents([texts[i] for i in new_indices])
    }

    collection.add(**to_add)
    print(f"✅ Added {len(to_add['ids'])} new chunks.")


def clear_chroma(path=CHROMA_PATH):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"🧹 Cleared Chroma DB at: {path}")
    else:
        print("ℹ️ No Chroma DB to clear.")


# -- Helpers --
def _load_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_hashes(h):
    with open(HASH_RECORD_FILE, "w") as f:
        json.dump(h, f, indent=2)

def _get_file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


# -- CLI Mode (only when run directly) --
if __name__ == "__main__":
    
    import argparse
    from app.tools import urlscraper_tool
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset Chroma vector DB")
    parser.add_argument("--data_path", type=str, default="data", help="PDF directory to load")
    parser.add_argument("--url", type=str, help="URL to scrape and ingest into ChromaDB")
    args = parser.parse_args()

    if args.reset:
        clear_chroma()
        exit()

    if args.url:
        print(f"🌐 Scraping from URL: {args.url}")
        result = urlscraper_tool.scrape_url_and_download_files(args.url, download_dir=args.data_path)

        # # Add webpage text to Chroma
        # if result["text"].strip():
        #     from langchain_core.documents import Document
        #     print("🧠 Processing webpage content...")
        #     chunks = split_documents([Document(page_content=result["text"])])
        #     chunks = assign_chunk_ids(chunks)
        #     add_to_chroma(chunks)

        # # Also process downloaded files (PDFs)
        # if result["downloaded_files"]:
        #     print(f"📎 Processing {len(result['downloaded_files'])} downloaded documents...")
        #     docs = load_documents(data_path=args.data_path)
        #     chunks = split_documents(docs)
        #     chunks = assign_chunk_ids(chunks)
        #     add_to_chroma(chunks)

    else:
        # Fallback to just local PDF ingestion
        docs = load_documents(args.data_path)
        chunks = split_documents(docs)
        chunks = assign_chunk_ids(chunks)
        add_to_chroma(chunks)

