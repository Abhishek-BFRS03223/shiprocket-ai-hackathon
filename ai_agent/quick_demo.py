#!/usr/bin/env python3
"""Quick demonstration of the AI agent in mock mode"""

from agent import ShiprocketAIAgent

def main():
    print("🎯 Mock Mode Demonstration:")
    
    agent = ShiprocketAIAgent()
    
    queries = [
        'What can you help me with?',
        'What\'s the weather in Mumbai?',
        'Calculate 25 * 4 + 10',
        'Search for laptop products',
        'Send email to test@example.com|Demo|Hello from AI agent'
    ]
    
    for i, query in enumerate(queries, 1):
        result = agent.process_query(query, f'demo_{i}')
        print(f'\nQuery {i}: {query}')
        print(f'Response: {result["response"][:120]}...')
        print(f'Status: {result["status"]}')

if __name__ == "__main__":
    main() 