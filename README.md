# Shiprocket AI Hackathon Project

This is a project for the Shiprocket AI Hackathon.

## Tech Stack

- Backend: Go (Gorilla Mux) with MongoDB, MySQL & PostgreSQL support (GORM)
- AI: OpenAI API
- Frontend: React (setup not included in this repo)

## Getting Started

1. Copy `env.example` to `.env` and fill in your environment variables (Mongo, MySQL, OpenAI…).
2. Ensure Go (≥1.20) is installed.
3. Run `go mod tidy` to download dependencies (if you add new imports).
4. Start the server:

```bash
go run .
```

The server will run on `http://localhost:3000` by default and expose a `/health` endpoint.

## Project Structure

- `controllers/` - API controllers
- `handlers/` - Request handlers
- `helpers/` - Utility functions
- `managers/` - Business logic managers

Feel free to add your own packages and code – the basic wiring is done so you can focus on features.

### Vector database (Python)

All RAG-related tooling lives in `vector/`.

```bash
# create venv & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r vector/requirements.txt

# ingest files into FAISS (default) or Chroma
python vector/ingest.py data/ --out vector_store

# change backend by setting env var
export VECTOR_DB=chroma
python vector/ingest.py data/ --out ./chroma_db
```

The script auto-selects OpenAI embeddings if `OPENAI_API_KEY` is present, otherwise falls back to a local HuggingFace model. 