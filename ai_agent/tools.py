"""
External Tools for LangChain Agents
Demonstrates integration with external APIs and services
"""

import requests
import json
from typing import Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class WeatherTool(BaseTool):
    """Tool to get weather information for a given city"""
    
    name: str = "weather_lookup"
    description: str = "Get current weather information for a specific city. Input should be a city name."
    
    def _run(self, city: str) -> str:
        """Get weather information using a mock API"""
        # Mock weather data - in real scenario, use OpenWeatherMap or similar API
        mock_weather = {
            "New York": {"temp": "22°C", "condition": "Sunny", "humidity": "65%"},
            "London": {"temp": "15°C", "condition": "Cloudy", "humidity": "80%"},
            "Mumbai": {"temp": "32°C", "condition": "Hot", "humidity": "75%"},
            "Delhi": {"temp": "28°C", "condition": "Clear", "humidity": "60%"}
        }
        
        weather_info = mock_weather.get(city, {
            "temp": "25°C", 
            "condition": "Unknown", 
            "humidity": "70%"
        })
        
        return f"Weather in {city}: Temperature: {weather_info['temp']}, " \
               f"Condition: {weather_info['condition']}, Humidity: {weather_info['humidity']}"


class CalculatorTool(BaseTool):
    """Tool to perform mathematical calculations"""
    
    name: str = "calculator"
    description: str = "Perform mathematical calculations. Input should be a mathematical expression as a string."
    
    def _run(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any potential dangerous operations
            safe_expression = expression.replace("__", "").replace("import", "").replace("exec", "")
            
            # Only allow basic mathematical operations
            allowed_chars = set("0123456789+-*/().,% ")
            if not all(c in allowed_chars for c in safe_expression):
                return "Error: Only basic mathematical operations are allowed"
            
            result = eval(safe_expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating expression '{expression}': {str(e)}"


class DatabaseSearchTool(BaseTool):
    """Tool to search mock database for information"""
    
    name: str = "database_search"
    description: str = "Search the database for product, order, or customer information. Input should be a search query."
    
    def _run(self, query: str) -> str:
        """Search mock database"""
        # Mock database - in real scenario, connect to your actual database
        mock_db = {
            "products": [
                {"id": 1, "name": "Laptop", "price": 50000, "stock": 25},
                {"id": 2, "name": "Mobile Phone", "price": 25000, "stock": 50},
                {"id": 3, "name": "Headphones", "price": 5000, "stock": 100}
            ],
            "orders": [
                {"id": 101, "customer": "John Doe", "product": "Laptop", "status": "Shipped"},
                {"id": 102, "customer": "Jane Smith", "product": "Mobile Phone", "status": "Processing"},
                {"id": 103, "customer": "Bob Wilson", "product": "Headphones", "status": "Delivered"}
            ]
        }
        
        query_lower = query.lower()
        results = []
        
        # Search products
        if "product" in query_lower or "laptop" in query_lower or "phone" in query_lower:
            for product in mock_db["products"]:
                if query_lower in product["name"].lower():
                    results.append(f"Product: {product['name']}, Price: ₹{product['price']}, Stock: {product['stock']}")
        
        # Search orders
        if "order" in query_lower or "customer" in query_lower:
            for order in mock_db["orders"]:
                if query_lower in order["customer"].lower() or query_lower in order["product"].lower():
                    results.append(f"Order {order['id']}: Customer: {order['customer']}, Product: {order['product']}, Status: {order['status']}")
        
        if not results:
            return f"No results found for query: {query}"
        
        return "Database search results:\n" + "\n".join(results)


class EmailTool(BaseTool):
    """Tool to send mock emails"""
    
    name: str = "send_email"
    description: str = "Send an email notification. Input should be 'recipient|subject|message' separated by pipes."
    
    def _run(self, email_data: str) -> str:
        """Send mock email"""
        try:
            parts = email_data.split("|")
            if len(parts) != 3:
                return "Error: Email data should be in format 'recipient|subject|message'"
            
            recipient, subject, message = parts
            
            # Mock email sending - in real scenario, use SMTP or email service
            return f"✅ Email sent successfully!\nTo: {recipient}\nSubject: {subject}\nMessage: {message[:50]}..."
        except Exception as e:
            return f"Error sending email: {str(e)}"


def get_available_tools() -> List[BaseTool]:
    """Return list of all available tools"""
    return [
        WeatherTool(),
        CalculatorTool(),
        DatabaseSearchTool(),
        EmailTool()
    ]


def get_tool_descriptions() -> str:
    """Get descriptions of all available tools"""
    tools = get_available_tools()
    descriptions = []
    
    for tool in tools:
        descriptions.append(f"- {tool.name}: {tool.description}")
    
    return "Available Tools:\n" + "\n".join(descriptions) 