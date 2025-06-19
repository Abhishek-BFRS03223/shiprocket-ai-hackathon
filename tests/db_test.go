package tests

import (
	"context"
	"testing"
	"time"

	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"

	"shiprocket-ai-hackathon-1/helpers"
)

// init runs before the tests. It loads env and connects to databases.
func init() {
	_ = godotenv.Load(".env") // ignore error if .env missing
	helpers.ConnectMongo()
	helpers.ConnectMySQL()
}

func TestMongoInsertAndQuery(t *testing.T) {
	if helpers.MongoClient == nil {
		t.Skip("MongoDB client not initialised (set MONGO_DB_CATALOG or MONGODB_URI)")
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	coll := helpers.MongoClient.Database("test_db").Collection("sample")
	doc := bson.M{"message": "hello", "ts": time.Now()}
	res, err := coll.InsertOne(ctx, doc)
	if err != nil {
		t.Fatalf("Mongo insert failed: %v", err)
	}

	var out bson.M
	if err := coll.FindOne(ctx, bson.M{"_id": res.InsertedID}).Decode(&out); err != nil {
		t.Fatalf("Mongo fetch failed: %v", err)
	}
}

func TestMySQLInsertAndQuery(t *testing.T) {
	if helpers.MySQLDB == nil {
		t.Skip("MySQL DB not initialised (set DATABASE_* env vars)")
	}

	type User struct {
		ID   uint   `gorm:"primaryKey"`
		Name string `gorm:"size:255"`
	}

	if err := helpers.MySQLDB.AutoMigrate(&User{}); err != nil {
		t.Fatalf("AutoMigrate: %v", err)
	}

	u := User{Name: "TestUser"}
	if err := helpers.MySQLDB.Create(&u).Error; err != nil {
		t.Fatalf("Insert: %v", err)
	}

	var count int64
	if err := helpers.MySQLDB.Model(&User{}).Where("id = ?", u.ID).Count(&count).Error; err != nil {
		t.Fatalf("Count: %v", err)
	}
	if count != 1 {
		t.Fatalf("Expected 1 row, got %d", count)
	}
}
