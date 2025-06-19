import os
import random
import shutil
import string
import tempfile

from dotenv import load_dotenv

load_dotenv()

VECTOR_DB = os.getenv("VECTOR_DB", "faiss").lower()


def random_doc(n_tokens: int = 500) -> str:
    return " ".join("".join(random.choices(string.ascii_lowercase, k=5)) for _ in range(n_tokens))


def main():
    tmpdir = tempfile.mkdtemp(prefix="vector_test_")
    try:
        # 1. Generate random text file
        txt_path = os.path.join(tmpdir, "sample.txt")
        with open(txt_path, "w") as f:
            f.write(random_doc())

        # 2. Import heavy deps lazily (speed CLI startup)
        from langchain.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        if VECTOR_DB == "faiss":
            from langchain.vectorstores import FAISS as VectorStore
        else:
            from langchain.vectorstores import Chroma as VectorStore
        from langchain.embeddings import OpenAIEmbeddings
        from langchain_community.embeddings import FakeEmbeddings

        # 3. Load & split
        docs = TextLoader(txt_path).load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = splitter.split_documents(docs)

        # 4. Pick embeddings backend
        embedder = OpenAIEmbeddings() if os.getenv("OPENAI_API_KEY") else FakeEmbeddings(size=768)

        # 5. Build vector store
        out_dir = os.path.join(tmpdir, "index")
        if VECTOR_DB == "faiss":
            vs = VectorStore.from_documents(splits, embedder)
            vs.save_local(out_dir)
            store = VectorStore.load_local(out_dir, embedder)
        else:
            vs = VectorStore.from_documents(splits, embedder, persist_directory=out_dir)
            vs.persist()
            store = VectorStore(persist_directory=out_dir, embedding_function=embedder)

        # 6. Query
        results = store.similarity_search("hello", k=1)
        assert results, "No results returned from similarity search"
        print(f"Vector DB test succeeded with backend {VECTOR_DB}. Returned {len(results)} doc(s)")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main() 