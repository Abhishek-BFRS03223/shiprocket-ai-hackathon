import os
import argparse
from pathlib import Path

from dotenv import load_dotenv

# Choose backend
VECTOR_DB = os.getenv("VECTOR_DB", "faiss").lower()

load_dotenv()

# Embeddings
try:
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
except ImportError as e:
    raise ImportError("Missing langchain core modules – install deps via 'pip install -r vector/requirements.txt'") from e

# Loaders & vector stores moved to langchain_community in 0.2+
try:
    from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter  # still in core

    if VECTOR_DB == "faiss":
        from langchain_community.vectorstores import FAISS as VectorStore
    elif VECTOR_DB == "chroma":
        from langchain_community.vectorstores import Chroma as VectorStore
    else:
        raise ValueError("Unsupported VECTOR_DB, choose 'faiss' or 'chroma'")
except ImportError as e:
    raise ImportError("Missing langchain-community modules – run 'pip install langchain-community' or update requirements") from e


def load_documents(paths):
    docs = []
    for p in paths:
        ext = p.suffix.lower()
        if ext == ".txt":
            docs.extend(TextLoader(str(p)).load())
        elif ext == ".csv":
            docs.extend(CSVLoader(str(p)).load())
        elif ext == ".pdf":
            docs.extend(PyPDFLoader(str(p)).load())
        else:
            print(f"Skipping unsupported file: {p}")
    return docs


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into a vector store")
    parser.add_argument("data_dir", help="Path to directory containing input docs (txt, csv, pdf)")
    parser.add_argument("--out", default="./vector_store", help="Output directory or file")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    files = [p for p in data_dir.rglob("*") if p.is_file()]
    print(f"Found {len(files)} files…")

    documents = load_documents(files)
    print(f"Loaded {len(documents)} docs")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(documents)

    # Embeddings: default OpenAI unless OPENAI_API_KEY missing
    if os.getenv("OPENAI_API_KEY"):
        embedder = OpenAIEmbeddings()
    else:
        embedder = HuggingFaceEmbeddings()

    vs = VectorStore.from_documents(splits, embedder)

    if VECTOR_DB == "faiss":
        vs.save_local(args.out)
    else:  # chroma
        os.makedirs(args.out, exist_ok=True)
        vs.persist()
    print("Vector store saved to", args.out)


if __name__ == "__main__":
    main() 