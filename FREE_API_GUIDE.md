# 🆓 FREE AI API ALTERNATIVES GUIDE
**Updated: January 2025**

This guide provides free AI API alternatives that you can use for your Shiprocket AI Hackathon project.

## 🔥 TOP FREE OPTIONS (No Credit Card Required)

### 1. **Groq (Best for Speed) - RECOMMENDED** 
- **API**: `https://api.groq.com/openai/v1/chat/completions`
- **Models**: Llama 3.1, Mixtral, Gemma 2
- **Free Tier**: 14,400 requests/day per model
- **Speed**: Extremely fast inference
- **Setup**: Get free API key at https://console.groq.com

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 2. **Hugging Face Inference API**
- **API**: `https://api-inference.huggingface.co/models/`
- **Models**: 100k+ open source models
- **Free Tier**: 1000 requests/day
- **Setup**: Get free token at https://huggingface.co/settings/tokens

```bash
export HF_API_TOKEN="your_hugging_face_token"
```

### 3. **DeepSeek API** 
- **API**: `https://api.deepseek.com/chat/completions`
- **Models**: DeepSeek V3, DeepSeek Coder
- **Free Tier**: $5 free credits monthly
- **Setup**: Sign up at https://platform.deepseek.com

### 4. **Anthropic Claude (Limited Free)**
- **Free Tier**: Available through claude.ai (web interface)
- **API**: Requires paid credits for API access
- **Alternative**: Use web scraping or Claude through other platforms

### 5. **Together AI**
- **API**: `https://api.together.xyz/v1/chat/completions`
- **Models**: Llama, Mixtral, Qwen models
- **Free Tier**: $5 credits on signup
- **Setup**: https://together.ai

## 🛠️ IMPLEMENTATION OPTIONS

### Option 1: Update AI Agent for Groq (RECOMMENDED)

Add to `ai_agent/config.py`:
```python
class Config:
    # Keep existing OpenAI config as fallback
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
    
    # Add Groq configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"
    GROQ_MODEL = "llama-3.1-70b-versatile"  # Fast and capable
    
    # Add API provider selection
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # groq, openai, huggingface
```

Update `ai_agent/agent.py`:
```python
def _initialize_components(self):
    """Initialize components with multiple API provider support"""
    try:
        provider = self.config.AI_PROVIDER.lower()
        
        if provider == "groq" and self.config.GROQ_API_KEY:
            # Use Groq API (OpenAI compatible)
            self.llm = ChatOpenAI(
                api_key=self.config.GROQ_API_KEY,
                base_url=self.config.GROQ_BASE_URL,
                model=self.config.GROQ_MODEL,
                temperature=0.7
            )
            print("✅ Using Groq API (Free)")
            
        elif provider == "openai" and self.api_key != "your_openai_api_key_here":
            # Use OpenAI API
            self.llm = ChatOpenAI(
                api_key=self.api_key,
                model=self.model,
                temperature=0.7
            )
            print("✅ Using OpenAI API")
            
        else:
            print("⚠️  No valid API key found, running in mock mode")
            self._initialize_mock_mode()
            return
            
        # Continue with rest of initialization...
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        self._initialize_mock_mode()
```

### Option 2: Hugging Face Integration

Create `ai_agent/huggingface_client.py`:
```python
import requests
import json
from typing import Dict, Any

class HuggingFaceClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def chat_completion(self, messages: list, model: str = "microsoft/DialoGPT-large"):
        """OpenAI-like chat completion using HF models"""
        url = f"{self.base_url}/{model}"
        
        # Convert messages to HF format
        prompt = self._messages_to_prompt(messages)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "choices": [{
                    "message": {
                        "content": result[0]["generated_text"] if result else "No response"
                    }
                }]
            }
        else:
            raise Exception(f"HF API Error: {response.text}")
    
    def _messages_to_prompt(self, messages: list) -> str:
        """Convert OpenAI messages to simple prompt"""
        prompt = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"Human: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "
        return prompt
```

## 🚀 QUICK SETUP COMMANDS

### Setup Groq (Fastest & Best Free Option):
```bash
# 1. Sign up at https://console.groq.com
# 2. Get your API key
# 3. Set environment variable
export GROQ_API_KEY="gsk_your_key_here"
export AI_PROVIDER="groq"

# 4. Test the agent
cd ai_agent
python clean_demo.py
```

### Setup Hugging Face:
```bash
# 1. Sign up at https://huggingface.co
# 2. Get token from https://huggingface.co/settings/tokens
# 3. Set environment variable
export HF_API_TOKEN="hf_your_token_here"
export AI_PROVIDER="huggingface"

# 4. Test the integration
cd ai_agent
python tools_demo.py
```

### Setup DeepSeek:
```bash
# 1. Sign up at https://platform.deepseek.com
# 2. Get $5 free credits
# 3. Get API key
export DEEPSEEK_API_KEY="your_deepseek_key"
```

## 📊 COMPARISON TABLE

| Provider | Free Tier | Speed | Quality | API Compatible | Best For |
|----------|-----------|-------|---------|----------------|----------|
| **Groq** | 14.4k/day | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ OpenAI | Speed & Volume |
| **HuggingFace** | 1k/day | ⚡⚡ | ⭐⭐⭐ | 🔧 Custom | Open Source |
| **DeepSeek** | $5/month | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ✅ OpenAI | Code Tasks |
| **Together AI** | $5 credits | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ OpenAI | Variety |

## 🎯 RECOMMENDATION FOR HACKATHON

**Use Groq** - Here's why:
1. **Highest free limits** (14,400 requests/day)
2. **Fastest inference** (crucial for demos)
3. **OpenAI compatible** (minimal code changes)
4. **No credit card required**
5. **Excellent model quality** (Llama 3.1 70B)

## 🔧 IMPLEMENTATION STEPS

1. **Get Groq API Key** (2 minutes):
   - Go to https://console.groq.com
   - Sign up with email
   - Go to API Keys section
   - Create new key

2. **Update Your Config** (1 minute):
   ```bash
   export GROQ_API_KEY="your_groq_key_here"
   export AI_PROVIDER="groq"
   ```

3. **Modify ai_agent/config.py** (add Groq config)

4. **Update ai_agent/agent.py** (add Groq support)

5. **Test Everything**:
   ```bash
   cd ai_agent
   python clean_demo.py
   python test_agent.py
   ```

## 🆘 BACKUP OPTIONS

If Groq hits limits:
1. **Switch to DeepSeek** (excellent for coding)
2. **Use HuggingFace** (good for experimentation)  
3. **Combine multiple providers** (load balancing)

## 🔄 EASY PROVIDER SWITCHING

Set in environment:
```bash
# Use Groq (default)
export AI_PROVIDER="groq"

# Switch to DeepSeek
export AI_PROVIDER="deepseek"

# Switch to HuggingFace
export AI_PROVIDER="huggingface"

# Fallback to mock mode
export AI_PROVIDER="mock"
```

## ✅ VERIFICATION

Test your setup:
```bash
cd ai_agent
python -c "
import os
print('🔧 API Configuration:')
print(f'Provider: {os.getenv(\"AI_PROVIDER\", \"not set\")}')
print(f'Groq Key: {\"✅ Set\" if os.getenv(\"GROQ_API_KEY\") else \"❌ Missing\"}')
print(f'HF Token: {\"✅ Set\" if os.getenv(\"HF_API_TOKEN\") else \"❌ Missing\"}')
"
```

## 🎉 RESULT

With these free APIs, you'll have:
- ✅ **Unlimited development** during hackathon
- ✅ **Real AI responses** (not mock mode)
- ✅ **Fast inference** for demos
- ✅ **Professional quality** outputs
- ✅ **No costs** or credit card required

**Your Shiprocket AI Agent will be fully functional with real AI capabilities!** 🚀 