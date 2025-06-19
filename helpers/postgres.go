package helpers

import (
	"log"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// DB is a global Postgres database connection.
var DB *gorm.DB

// ConnectPostgres establishes a connection to Postgres using POSTGRES_DSN env var.
func ConnectPostgres() {
	dsn := os.Getenv("POSTGRES_DSN")
	if dsn == "" {
		log.Println("POSTGRES_DSN not provided, skipping Postgres connection")
		return
	}

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to Postgres: %v", err)
	}

	DB = db
	log.Println("Connected to Postgres")
}
