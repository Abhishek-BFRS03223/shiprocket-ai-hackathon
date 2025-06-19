"""
Memory Management for LangChain Agents
Demonstrates different types of memory for maintaining context across conversations
"""

from typing import Dict, List, Any
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryBufferMemory,
    ConversationTokenBufferMemory
)
from langchain_openai import ChatOpenAI
import json
import os


class AgentMemoryManager:
    """Manages different types of memory for AI agents"""
    
    def __init__(self, openai_api_key: str, max_tokens: int = 4000):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        self.max_tokens = max_tokens
        self.memory_store = {}
        
    def create_buffer_memory(self, session_id: str) -> ConversationBufferMemory:
        """Create simple buffer memory that stores all conversation history"""
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )
        self.memory_store[f"{session_id}_buffer"] = memory
        return memory
    
    def create_summary_memory(self, session_id: str) -> ConversationSummaryBufferMemory:
        """Create summary memory that summarizes old conversations"""
        memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output",
            max_token_limit=self.max_tokens
        )
        self.memory_store[f"{session_id}_summary"] = memory
        return memory
    
    def create_token_buffer_memory(self, session_id: str) -> ConversationTokenBufferMemory:
        """Create token-limited memory that keeps conversation within token limits"""
        memory = ConversationTokenBufferMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output",
            max_token_limit=self.max_tokens
        )
        self.memory_store[f"{session_id}_token"] = memory
        return memory
    
    def get_memory(self, session_id: str, memory_type: str = "buffer"):
        """Retrieve memory for a specific session"""
        memory_key = f"{session_id}_{memory_type}"
        
        if memory_key not in self.memory_store:
            if memory_type == "summary":
                return self.create_summary_memory(session_id)
            elif memory_type == "token":
                return self.create_token_buffer_memory(session_id)
            else:
                return self.create_buffer_memory(session_id)
        
        return self.memory_store[memory_key]
    
    def add_interaction(self, session_id: str, human_input: str, ai_output: str, memory_type: str = "buffer"):
        """Add a conversation interaction to memory"""
        memory = self.get_memory(session_id, memory_type)
        memory.save_context(
            {"input": human_input},
            {"output": ai_output}
        )
    
    def get_conversation_history(self, session_id: str, memory_type: str = "buffer") -> str:
        """Get formatted conversation history"""
        memory = self.get_memory(session_id, memory_type)
        history = memory.load_memory_variables({})
        
        if "chat_history" in history:
            messages = history["chat_history"]
            formatted_history = []
            
            for msg in messages:
                if hasattr(msg, 'content'):
                    role = "Human" if msg.type == "human" else "AI"
                    formatted_history.append(f"{role}: {msg.content}")
            
            return "\n".join(formatted_history)
        
        return "No conversation history found."
    
    def clear_memory(self, session_id: str, memory_type: str = "buffer"):
        """Clear memory for a specific session"""
        memory_key = f"{session_id}_{memory_type}"
        if memory_key in self.memory_store:
            del self.memory_store[memory_key]
    
    def save_memory_to_file(self, session_id: str, filename: str, memory_type: str = "buffer"):
        """Save memory to a JSON file"""
        history = self.get_conversation_history(session_id, memory_type)
        
        data = {
            "session_id": session_id,
            "memory_type": memory_type,
            "conversation_history": history,
            "timestamp": str(os.path.getmtime(__file__) if os.path.exists(__file__) else "unknown")
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_memory_from_file(self, filename: str) -> Dict[str, Any]:
        """Load memory from a JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Memory file not found"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory usage"""
        stats = {
            "total_sessions": len(set([key.split('_')[0] for key in self.memory_store.keys()])),
            "total_memories": len(self.memory_store),
            "memory_types": {},
            "sessions": []
        }
        
        for key in self.memory_store.keys():
            session_id, memory_type = key.rsplit('_', 1)
            
            if memory_type not in stats["memory_types"]:
                stats["memory_types"][memory_type] = 0
            stats["memory_types"][memory_type] += 1
            
            if session_id not in [s["id"] for s in stats["sessions"]]:
                stats["sessions"].append({
                    "id": session_id,
                    "memory_types": [memory_type]
                })
            else:
                for session in stats["sessions"]:
                    if session["id"] == session_id:
                        session["memory_types"].append(memory_type)
        
        return stats


class VectorMemoryManager:
    """Manages vector-based semantic memory using FAISS"""
    
    def __init__(self, openai_api_key: str, index_path: str = "ai_agent/vector_store"):
        self.openai_api_key = openai_api_key
        self.index_path = index_path
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize FAISS vector store"""
        try:
            from langchain_openai import OpenAIEmbeddings
            from langchain_community.vectorstores import FAISS
            
            self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
            
            # Try to load existing vector store
            if os.path.exists(self.index_path):
                self.vector_store = FAISS.load_local(
                    self.index_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                # Create new vector store with initial documents
                initial_docs = [
                    "Welcome to Shiprocket AI Assistant. I can help with orders, products, and shipping.",
                    "Shiprocket is a logistics platform that helps businesses with shipping and order management.",
                    "Common queries include order tracking, shipping rates, and delivery status."
                ]
                
                from langchain.schema import Document
                documents = [Document(page_content=doc) for doc in initial_docs]
                
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
                self.save_vector_store()
                
        except Exception as e:
            print(f"Warning: Could not initialize vector store: {e}")
            self.vector_store = None
    
    def add_to_memory(self, text: str, metadata: Dict[str, Any] = None):
        """Add text to vector memory"""
        if self.vector_store is None:
            return False
        
        try:
            from langchain.schema import Document
            doc = Document(page_content=text, metadata=metadata or {})
            self.vector_store.add_documents([doc])
            self.save_vector_store()
            return True
        except Exception as e:
            print(f"Error adding to vector memory: {e}")
            return False
    
    def search_similar(self, query: str, k: int = 3) -> List[str]:
        """Search for similar content in vector memory"""
        if self.vector_store is None:
            return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error searching vector memory: {e}")
            return []
    
    def save_vector_store(self):
        """Save vector store to disk"""
        if self.vector_store is not None:
            try:
                os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
                self.vector_store.save_local(self.index_path)
            except Exception as e:
                print(f"Error saving vector store: {e}")


def create_memory_demo():
    """Create a demonstration of different memory types"""
    return {
        "buffer_memory": "Stores complete conversation history",
        "summary_memory": "Summarizes old conversations to save tokens",
        "token_buffer_memory": "Keeps conversations within token limits",
        "vector_memory": "Enables semantic search across conversation history"
    } 