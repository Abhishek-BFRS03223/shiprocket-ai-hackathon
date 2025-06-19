package helpers

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

// MySQLDB is a global MySQL database connection.
var MySQLDB *gorm.DB

// ConnectMySQL establishes a connection to MySQL using env vars.
func ConnectMySQL() {
	dbName := os.Getenv("DATABASE_DATABASE")
	host := os.Getenv("DATABASE_HOST")
	port := os.Getenv("DATABASE_PORT")
	user := os.Getenv("DATABASE_USER")
	pass := os.Getenv("DATABASE_PASSWORD")

	if dbName == "" || host == "" || user == "" {
		log.Println("MySQL env vars not fully set, skipping MySQL connection")
		return
	}

	if port == "" {
		port = "3306"
	}

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=True&loc=Local", user, pass, host, port, dbName)

	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to MySQL: %v", err)
	}

	MySQLDB = db
	log.Println("Connected to MySQL")
}
