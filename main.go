package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"

	"shiprocket-ai-hackathon-1/handlers"
	"shiprocket-ai-hackathon-1/helpers"
)

func main() {
	// Load environment variables from .env if present
	_ = godotenv.Load()

	// Initialize external services
	helpers.ConnectMongo()
	helpers.ConnectPostgres()
	helpers.InitOpenAI()

	// Setup router
	r := mux.NewRouter()

	// Health check
	r.HandleFunc("/health", handlers.HealthHandler).Methods("GET")

	// TODO: add your routes here

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("Server running on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
