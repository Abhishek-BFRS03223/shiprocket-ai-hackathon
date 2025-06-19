#!/bin/bash

echo "=== SHIPROCKET AI HACKATHON - SERVICE STATUS CHECK ==="
echo ""

# Check Go Backend
echo "🔧 Checking Go Backend (http://localhost:3000)..."
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Go Backend: RUNNING"
    curl -s http://localhost:3000/health
else
    echo "❌ Go Backend: NOT RUNNING"
    echo "   Start with: go run main.go"
fi
echo ""

# Check React Frontend
echo "🎨 Checking React Frontend (http://localhost:5174)..."
if curl -s http://localhost:5174 > /dev/null 2>&1; then
    echo "✅ React Frontend: RUNNING"
else
    echo "❌ React Frontend: NOT RUNNING"
    echo "   Start with: cd frontend && npm run dev"
fi
echo ""

# Check MongoDB
echo "🍃 Checking MongoDB Connection..."
if mongosh "mongodb://abhishek.soni:mongo1234@sr-channel-catalog-mongo.localhost/sr-channel-catalog" --eval "db.runCommand('ping')" > /dev/null 2>&1; then
    echo "✅ MongoDB: CONNECTED"
else
    echo "❌ MongoDB: CONNECTION FAILED"
fi
echo ""

# Check MySQL
echo "🐬 Checking MySQL Connection..."
if mysql -h localhost -P 3306 -u root -pAdmin@1234 -D sr-ai-hack -e "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ MySQL: CONNECTED"
else
    echo "❌ MySQL: CONNECTION FAILED"
fi
echo ""

echo "=== STATUS CHECK COMPLETE ===" 