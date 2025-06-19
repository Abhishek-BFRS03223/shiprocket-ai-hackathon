package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"

	"shiprocket-ai-hackathon-1/helpers"
)

func main() {
	_ = godotenv.Load()
	helpers.ConnectMongo()
	helpers.ConnectMySQL()

	seedMongo()
	seedMySQL()
}

func seedMongo() {
	if helpers.MongoClient == nil {
		log.Println("MongoDB not initialised – skipping mongo seed")
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	coll := helpers.MongoClient.Database("catalog").Collection("products")

	doc := bson.M{"name": "Sample Product", "price": 9.99, "ts": time.Now()}
	res, err := coll.InsertOne(ctx, doc)
	if err != nil {
		log.Fatalf("Mongo seed insert failed: %v", err)
	}
	fmt.Printf("Inserted sample document into MongoDB with ID %v\n", res.InsertedID)
}

func seedMySQL() {
	if helpers.MySQLDB == nil {
		log.Println("MySQL not initialised – skipping mysql seed")
		return
	}

	type Product struct {
		ID    uint   `gorm:"primaryKey"`
		Name  string `gorm:"size:255"`
		Price float64
	}

	if err := helpers.MySQLDB.AutoMigrate(&Product{}); err != nil {
		log.Fatalf("MySQL migrate: %v", err)
	}

	p := Product{Name: "Sample Product", Price: 9.99}
	if err := helpers.MySQLDB.Create(&p).Error; err != nil {
		log.Fatalf("MySQL insert: %v", err)
	}
	fmt.Printf("Inserted sample row into MySQL with ID %d\n", p.ID)
}
