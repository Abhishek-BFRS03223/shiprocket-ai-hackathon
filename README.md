# Shiprocket AI Hackathon Project

This is a project for the Shiprocket AI Hackathon.

## Tech Stack

- Backend: Go (Gorilla Mux) with MongoDB and PostgreSQL support (GORM)
- AI: OpenAI API
- Frontend: React (setup not included in this repo)

## Getting Started

1. Copy `env.example` to `.env` and fill in your environment variables.
2. Ensure Go (≥1.20) is installed.
3. Run `go mod tidy` to download dependencies.
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