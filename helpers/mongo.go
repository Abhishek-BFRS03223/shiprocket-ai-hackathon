package helpers

import (
	"context"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// MongoClient is a global MongoDB client instance.
var MongoClient *mongo.Client

// ConnectMongo establishes a connection to MongoDB using the MONGODB_URI environment variable.
func ConnectMongo() {
	uri := os.Getenv("MONGODB_URI")
	if uri == "" {
		// Default local URI if not provided
		uri = "mongodb://localhost:27017"
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(uri))
	if err != nil {
		log.Fatalf("MongoDB connection error: %v", err)
	}

	// Verify connection
	if err = client.Ping(ctx, nil); err != nil {
		log.Fatalf("MongoDB ping error: %v", err)
	}

	MongoClient = client
	log.Println("Connected to MongoDB")
}
