# Shiprocket AI Agent with LangChain

A comprehensive AI agent implementation demonstrating **context-aware AI agents**, **external tool calling**, and **memory management** using LangChain framework.

## 🚀 Features

### ✅ **Context-Aware AI Agents**
- **Smart Context Retrieval**: Uses vector embeddings to find relevant conversation history
- **Session Management**: Maintains context across multiple conversation sessions
- **Contextual Responses**: Enhances responses using previous conversation context

### ✅ **External Tool Calling**
- **Weather Tool**: Get weather information for any city
- **Calculator Tool**: Perform mathematical calculations safely
- **Database Search Tool**: Search mock database for products and orders
- **Email Tool**: Send email notifications with formatted content

### ✅ **Memory Management**
- **Buffer Memory**: Stores complete conversation history
- **Summary Memory**: Summarizes old conversations to save tokens
- **Token Buffer Memory**: Keeps conversations within token limits
- **Vector Memory**: Enables semantic search across conversation history

### ✅ **Multiple LLM Support**
- **OpenAI GPT Models**: Primary integration with GPT-3.5-turbo/GPT-4
- **Anthropic Claude**: Ready for Claude integration
- **Local LLMs**: Extensible to local model support

## 📁 Project Structure

```
ai_agent/
├── requirements.txt       # Python dependencies
├── config.py             # Configuration management
├── tools.py              # External tools implementation
├── memory_manager.py     # Memory management classes
├── agent.py              # Main AI agent implementation
├── test_agent.py         # Comprehensive test suite
└── README.md             # This documentation
```

## ⚙️ Setup Instructions

### 1. **Activate Virtual Environment**
```bash
source langchain_env/bin/activate
```

### 2. **Install Dependencies**
```bash
pip install -r ai_agent/requirements.txt
```

### 3. **Set OpenAI API Key** (Optional for full functionality)
```bash
# Option 1: Environment variable
export OPENAI_API_KEY="your_actual_openai_api_key_here"

# Option 2: Edit config.py
# Update OPENAI_API_KEY in ai_agent/config.py
```

### 4. **Run Tests**
```bash
cd ai_agent
python test_agent.py
```

### 5. **Interactive Mode**
```bash
python agent.py
```

## 🧪 Testing & Demonstration

### **Comprehensive Test Suite**
```bash
python test_agent.py
```

**Test Coverage:**
- ✅ External Tools (Weather, Calculator, Database, Email)
- ✅ Memory Management (Multiple memory types)
- ✅ AI Agent Core (Query processing, context awareness)
- ✅ Integration Scenarios (Customer support, product workflows)

### **Sample Test Output**
```
🚀 Shiprocket AI Agent - Comprehensive Test Suite
============================================================

🔧 Testing External Tools...
✅ Found 4 tools:
  - weather_lookup: Get current weather information for a specific city
  - calculator: Perform mathematical calculations
  - database_search: Search the database for product, order, or customer information
  - send_email: Send an email notification

📊 TEST REPORT
==================================================
Total Tests: 4
Passed: 4
Failed: 0
Success Rate: 100.0%
```

## 🎯 Usage Examples

### **1. Basic Agent Usage**
```python
from agent import ShiprocketAIAgent

# Create agent
agent = ShiprocketAIAgent()

# Process query
result = agent.process_query("What's the weather in Mumbai?", "session_1")
print(result['response'])
```

### **2. Tool Calling Examples**
```python
# Weather query
result = agent.process_query("What's the weather in Delhi?")

# Calculator query
result = agent.process_query("Calculate 25 * 4 + 15")

# Database search
result = agent.process_query("Search for laptop orders")

# Email sending
result = agent.process_query("Send email to customer@example.com|Order Update|Your order has been shipped")
```

### **3. Memory Management**
```python
from memory_manager import AgentMemoryManager

# Create memory manager
memory_manager = AgentMemoryManager(api_key="your_key")

# Add interaction
memory_manager.add_interaction(
    "session_1",
    "My name is John and I'm from Mumbai",
    "Hello John! I'll remember that you're from Mumbai."
)

# Get conversation history
history = memory_manager.get_conversation_history("session_1")
```

### **4. Context-Aware Conversations**
```python
# Session with context memory
session_id = "customer_support"

# First query
agent.process_query("My name is Sarah and I ordered a laptop", session_id)

# Follow-up query (agent remembers context)
result = agent.process_query("What's the status of my order?", session_id)
# Agent will use previous context about Sarah and her laptop order
```

## 🔧 Technical Details

### **Compatible Package Versions**
- **LangChain**: 0.3.13 (Latest stable)
- **OpenAI**: 1.58.1 (Compatible with LangChain)
- **FAISS**: 1.9.0 (Vector database)
- **Python**: 3.10+ (Tested on 3.10.12)

### **Memory Types**
1. **Buffer Memory**: Stores complete conversation
2. **Summary Memory**: Auto-summarizes to fit token limits
3. **Token Buffer**: Hard token limit enforcement
4. **Vector Memory**: Semantic search capability

### **Error Handling**
- **Mock Mode**: Graceful fallback when OpenAI API unavailable
- **Tool Safety**: Secure evaluation of mathematical expressions
- **Memory Persistence**: Conversation history can be saved/loaded

## 🛠️ Customization

### **Adding New Tools**
```python
# In tools.py
class CustomTool(BaseTool):
    name: str = "custom_tool"
    description: str = "Description of what this tool does"
    
    def _run(self, input_param: str) -> str:
        # Tool implementation
        return "Tool result"
```

### **Custom Memory Types**
```python
# In memory_manager.py
def create_custom_memory(self, session_id: str):
    # Implement custom memory logic
    pass
```

### **Agent Configuration**
```python
# In config.py
class Config:
    AGENT_MAX_ITERATIONS = 10  # Adjust as needed
    MAX_MEMORY_TOKENS = 4000   # Memory limit
    AGENT_VERBOSE = True       # Debug output
```

## 🔍 Monitoring & Debugging

### **Agent Information**
```python
info = agent.get_agent_info()
print(json.dumps(info, indent=2))
```

### **Memory Statistics**
```python
stats = agent.memory_manager.get_memory_stats()
print(f"Active sessions: {stats['total_sessions']}")
```

### **Conversation History**
```python
history = agent.get_conversation_history("session_id")
print(history)
```

## 🚀 Integration with Shiprocket Backend

### **Go Backend Integration**
The agent can be integrated with your Go backend using HTTP endpoints:

```python
# Example integration endpoint
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    query = data.get('prompt')
    session_id = data.get('session_id', 'default')
    
    result = agent.process_query(query, session_id)
    return jsonify(result)
```

### **Database Integration**
Replace mock database in `tools.py` with real database connections:

```python
# In DatabaseSearchTool._run()
# Replace mock_db with real MongoDB/MySQL queries
from your_db_module import query_database
results = query_database(query)
```

## 📈 Performance Considerations

- **Token Management**: Automatic memory summarization prevents token overflow
- **Caching**: Vector embeddings cached for faster retrieval
- **Async Support**: Ready for async operations with proper imports
- **Error Recovery**: Graceful degradation when services unavailable

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Add tests** for new functionality
4. **Update documentation**
5. **Submit pull request**

## 📚 Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FAISS Documentation](https://faiss.ai/)
- [Shiprocket API Documentation](https://docs.shiprocket.in/)

---

**🎉 Your AI agent is ready for hackathon development!**

*This implementation demonstrates production-ready patterns for context-aware AI agents with external tool integration and comprehensive memory management.* 