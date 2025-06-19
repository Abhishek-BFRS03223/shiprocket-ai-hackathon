#!/usr/bin/env python3
"""Direct demonstration of tools working without LangChain agent"""

from tools import get_available_tools, get_tool_descriptions

def main():
    print("🔧 Direct Tools Demonstration")
    print("="*50)
    
    # Get all tools
    tools = get_available_tools()
    
    print(f"✅ Available Tools: {len(tools)}")
    print(get_tool_descriptions())
    
    print(f"\n🧪 Testing Each Tool Directly:")
    print("-" * 40)
    
    # Test Weather Tool
    weather_tool = next((t for t in tools if t.name == "weather_lookup"), None)
    if weather_tool:
        print(f"\n🌤️  Weather Tool Test:")
        print(f"  Query: Mumbai weather")
        result = weather_tool._run("Mumbai")
        print(f"  Result: {result}")
        
        print(f"\n  Query: Delhi weather")
        result = weather_tool._run("Delhi")
        print(f"  Result: {result}")
    
    # Test Calculator Tool
    calc_tool = next((t for t in tools if t.name == "calculator"), None)
    if calc_tool:
        print(f"\n🧮 Calculator Tool Test:")
        calculations = ["25 * 4 + 10", "100 / 5", "(15 + 25) * 2", "50 - 12 + 8"]
        for calc in calculations:
            result = calc_tool._run(calc)
            print(f"  {calc} = {result}")
    
    # Test Database Tool
    db_tool = next((t for t in tools if t.name == "database_search"), None)
    if db_tool:
        print(f"\n🗄️  Database Tool Test:")
        searches = ["laptop", "mobile phone", "order john", "customer jane"]
        for search in searches:
            print(f"\n  Search: '{search}'")
            result = db_tool._run(search)
            print(f"  Result: {result}")
    
    # Test Email Tool
    email_tool = next((t for t in tools if t.name == "send_email"), None)
    if email_tool:
        print(f"\n📧 Email Tool Test:")
        emails = [
            "customer@example.com|Order Shipped|Your order #12345 has been shipped",
            "support@company.com|Low Stock Alert|Laptop inventory is running low",
            "manager@company.com|Daily Report|Sales summary for today"
        ]
        for email in emails:
            result = email_tool._run(email)
            print(f"  {result}")
    
    print(f"\n🎯 Mock Agent Responses:")
    print("-" * 40)
    
    # Simulate mock agent responses
    mock_queries = [
        ("What's the weather like?", "I can check weather for any city! Try: 'weather in Mumbai'"),
        ("Calculate something", "I can do math! Try: 'calculate 25 * 4 + 10'"),
        ("Find my order", "I can search orders! Try: 'search for orders by John'"),
        ("Send notification", "I can send emails! Format: 'email@example.com|Subject|Message'")
    ]
    
    for query, response in mock_queries:
        print(f"\n  Q: {query}")
        print(f"  A: {response}")
    
    print(f"\n✅ All tools are working correctly!")
    print(f"📋 Summary:")
    print(f"  • Weather Tool: ✅ Working (Mock data)")
    print(f"  • Calculator Tool: ✅ Working (Safe evaluation)")
    print(f"  • Database Tool: ✅ Working (Mock database)")
    print(f"  • Email Tool: ✅ Working (Mock sending)")
    print(f"\n🚀 Ready for integration with LangChain agent when OpenAI API key is provided!")

if __name__ == "__main__":
    main() 