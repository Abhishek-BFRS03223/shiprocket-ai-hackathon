"""
Context-Aware AI Agent using LangChain
Demonstrates agent workflows with external tools and memory management
"""

import os
import sys
from typing import Dict, List, Any, Optional

# Handle imports for both direct execution and module import
try:
    from config import Config
    from tools import get_available_tools, get_tool_descriptions
    from memory_manager import AgentMemoryManager, VectorMemoryManager
except ImportError:
    # If running from different directory, try to add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from config import Config
    from tools import get_available_tools, get_tool_descriptions
    from memory_manager import AgentMemoryManager, VectorMemoryManager

try:
    from langchain.agents import AgentType, initialize_agent
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("Warning: LangChain imports not available. Running in mock mode.")
    LANGCHAIN_AVAILABLE = False


class ShiprocketAIAgent:
    """
    Context-aware AI Agent for Shiprocket operations
    Features:
    - External tool calling (weather, calculator, database, email)
    - Memory management across conversations
    - Context awareness
    - Multiple LLM support (OpenAI, Anthropic)
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        self.config = Config()
        
        # Initialize components
        self.llm = None
        self.agent = None
        self.memory_manager = None
        self.vector_memory = None
        self.tools = []
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all agent components"""
        try:
            if LANGCHAIN_AVAILABLE and self.api_key != "your_openai_api_key_here":
                # Initialize LLM
                self.llm = ChatOpenAI(
                    api_key=self.api_key,
                    model=self.model,
                    temperature=0.7
                )
                
                # Initialize tools
                self.tools = get_available_tools()
                
                # Initialize memory managers
                self.memory_manager = AgentMemoryManager(
                    openai_api_key=self.api_key,
                    max_tokens=self.config.MAX_MEMORY_TOKENS
                )
                
                self.vector_memory = VectorMemoryManager(
                    openai_api_key=self.api_key,
                    index_path=self.config.FAISS_INDEX_PATH
                )
                
                # Initialize agent
                self.agent = initialize_agent(
                    tools=self.tools,
                    llm=self.llm,
                    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                    verbose=self.config.AGENT_VERBOSE,
                    max_iterations=self.config.AGENT_MAX_ITERATIONS,
                    memory=self.memory_manager.create_buffer_memory("default")
                )
                
                print("✅ AI Agent initialized successfully with full functionality!")
            else:
                print("⚠️  Running in MOCK mode - Set OPENAI_API_KEY for full functionality")
                self._initialize_mock_mode()
                
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            self._initialize_mock_mode()
    
    def _initialize_mock_mode(self):
        """Initialize mock mode when LangChain is not available"""
        self.tools = get_available_tools()
        print("🔧 Mock mode initialized with tools:", [tool.name for tool in self.tools])
    
    def process_query(self, query: str, session_id: str = "default", 
                     memory_type: str = "buffer") -> Dict[str, Any]:
        """
        Process a user query with context awareness
        
        Args:
            query: User input query
            session_id: Session identifier for memory management
            memory_type: Type of memory to use (buffer, summary, token)
        
        Returns:
            Dict containing response and metadata
        """
        
        # Get relevant context from vector memory
        context = self._get_relevant_context(query)
        
        # Enhance query with context
        enhanced_query = self._enhance_query_with_context(query, context)
        
        if self.agent and LANGCHAIN_AVAILABLE:
            try:
                # Get memory for this session
                memory = self.memory_manager.get_memory(session_id, memory_type)
                self.agent.memory = memory
                
                # Process with agent
                response = self.agent.run(enhanced_query)
                
                # Add to vector memory for future context
                self.vector_memory.add_to_memory(
                    f"Q: {query}\nA: {response}",
                    {"session_id": session_id, "type": "conversation"}
                )
                
                return {
                    "response": response,
                    "session_id": session_id,
                    "memory_type": memory_type,
                    "context_used": context,
                    "tools_available": [tool.name for tool in self.tools],
                    "status": "success"
                }
                
            except Exception as e:
                return {
                    "response": f"Error processing query: {str(e)}",
                    "session_id": session_id,
                    "status": "error"
                }
        
        else:
            # Mock response when agent is not available
            return self._generate_mock_response(query, session_id, context)
    
    def _get_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """Get relevant context from vector memory"""
        if self.vector_memory:
            return self.vector_memory.search_similar(query, k)
        return []
    
    def _enhance_query_with_context(self, query: str, context: List[str]) -> str:
        """Enhance user query with relevant context"""
        if not context:
            return query
        
        context_str = "\n".join([f"- {ctx}" for ctx in context])
        enhanced = f"""
Context from previous conversations:
{context_str}

Current question: {query}

Please use the context above to provide a more informed response.
"""
        return enhanced.strip()
    
    def _generate_mock_response(self, query: str, session_id: str, context: List[str]) -> Dict[str, Any]:
        """Generate mock response when full agent is not available"""
        
        # Simple keyword-based responses
        query_lower = query.lower()
        
        if "weather" in query_lower:
            response = "I'd check the weather for you, but I need a valid OpenAI API key to access the weather tool."
        elif "calculate" in query_lower or any(op in query_lower for op in ["+", "-", "*", "/", "="]):
            response = "I can help with calculations! For example, try asking 'calculate 25 * 4 + 10'"
        elif "order" in query_lower or "product" in query_lower:
            response = "I can search the database for order and product information. Try asking about 'laptop orders' or 'product inventory'."
        elif "email" in query_lower:
            response = "I can help send email notifications. Format: 'send email to user@example.com|Subject|Message content'"
        else:
            response = f"Hello! I'm the Shiprocket AI Assistant. I can help with:\n{get_tool_descriptions()}\n\nTo enable full functionality, please set your OPENAI_API_KEY."
        
        return {
            "response": response,
            "session_id": session_id,
            "memory_type": "mock",
            "context_used": context,
            "tools_available": [tool.name for tool in self.tools],
            "status": "mock_mode"
        }
    
    def get_conversation_history(self, session_id: str = "default", 
                                memory_type: str = "buffer") -> str:
        """Get conversation history for a session"""
        if self.memory_manager:
            return self.memory_manager.get_conversation_history(session_id, memory_type)
        return "Memory manager not available in mock mode."
    
    def clear_session_memory(self, session_id: str = "default", 
                            memory_type: str = "buffer"):
        """Clear memory for a specific session"""
        if self.memory_manager:
            self.memory_manager.clear_memory(session_id, memory_type)
            return f"Memory cleared for session {session_id} ({memory_type})"
        return "Memory manager not available."
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent's capabilities"""
        return {
            "agent_type": "ShiprocketAIAgent",
            "model": self.model,
            "langchain_available": LANGCHAIN_AVAILABLE,
            "api_key_configured": self.api_key != "your_openai_api_key_here",
            "tools_available": [tool.name for tool in self.tools],
            "memory_types": ["buffer", "summary", "token", "vector"],
            "features": [
                "Context-aware responses",
                "External tool calling",
                "Memory management",
                "Multi-session support",
                "Vector-based semantic search"
            ]
        }
    
    def demonstrate_capabilities(self) -> Dict[str, Any]:
        """Demonstrate the agent's capabilities"""
        demo_queries = [
            "What's the weather in Mumbai?",
            "Calculate 15 * 8 + 25",
            "Search for laptop orders",
            "Send email to customer@example.com|Order Update|Your order has been shipped"
        ]
        
        results = {}
        for i, query in enumerate(demo_queries):
            results[f"demo_{i+1}"] = self.process_query(query, f"demo_session_{i+1}")
        
        return {
            "demonstrations": results,
            "agent_info": self.get_agent_info(),
            "memory_stats": self.memory_manager.get_memory_stats() if self.memory_manager else {}
        }


def create_agent_demo():
    """Create and demonstrate the AI agent"""
    print("🚀 Creating Shiprocket AI Agent Demo...")
    
    # Create agent
    agent = ShiprocketAIAgent()
    
    # Show agent info
    info = agent.get_agent_info()
    print(f"\n📋 Agent Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Demonstrate capabilities
    print(f"\n🎭 Demonstrating capabilities...")
    demo_results = agent.demonstrate_capabilities()
    
    return agent, demo_results


if __name__ == "__main__":
    agent, demo = create_agent_demo()
    
    # Interactive mode
    print(f"\n💬 Interactive Mode (type 'quit' to exit):")
    session_id = "interactive_session"
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if user_input:
                result = agent.process_query(user_input, session_id)
                print(f"\nAI: {result['response']}")
                
                if result['status'] == 'success':
                    print(f"[Context used: {len(result['context_used'])} items]")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print(f"\n📊 Final Memory Stats:")
    if agent.memory_manager:
        stats = agent.memory_manager.get_memory_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}") 