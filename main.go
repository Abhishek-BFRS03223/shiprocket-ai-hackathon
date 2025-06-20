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
	helpers.ConnectMySQL()
	helpers.InitOpenAI()

	// Setup router
	r := mux.NewRouter()

	// API routes
	api := r.PathPrefix("/api").Subrouter()

	// Health check
	api.HandleFunc("/health", handlers.HealthHandler).Methods("GET")

	// Site Generator API routes
	api.HandleFunc("/generate", handlers.GenerateSiteHandler).Methods("POST", "OPTIONS")
	api.HandleFunc("/sites", handlers.ListSitesHandler).Methods("GET", "OPTIONS")
	api.HandleFunc("/sites/{siteName}", handlers.ViewSiteHandler).Methods("GET", "OPTIONS")
	api.HandleFunc("/demo/generate", handlers.DemoGenerateHandler).Methods("POST", "OPTIONS")

	// Static file serving for generated sites
	r.PathPrefix("/generated/").Handler(http.StripPrefix("/generated/", http.FileServer(http.Dir("./generated_sites/"))))

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	log.Printf("🚀 Server running on port %s", port)
	log.Printf("📊 Health check: http://localhost:%s/api/health", port)
	log.Printf("🎯 Site Generator: http://localhost:%s/api/generate", port)
	log.Printf("📝 Generated Sites: http://localhost:%s/api/sites", port)
	log.Printf("🔥 Demo Generator: http://localhost:%s/api/demo/generate", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
