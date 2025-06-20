"""
One-Click Site Generator
Main orchestrator for generating complete websites from product names
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Add the ai_agent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from langchain.agents import initialize_agent, AgentType
    from langchain.memory import ConversationBufferMemory
    from langchain_openai import ChatOpenAI
    from site_generator_tools import get_site_generator_tools
    from config import get_openai_api_key, get_langchain_settings
except ImportError as e:
    print(f"Warning: LangChain import failed: {e}")
    print("Running in mock mode")

class OneClickSiteGenerator:
    """One-click website generator from product names"""
    
    def __init__(self, openai_api_key: Optional[str] = None, use_mock: bool = False):
        """Initialize the site generator"""
        self.use_mock = use_mock
        self.openai_api_key = openai_api_key or get_openai_api_key()
        
        if not self.use_mock and self.openai_api_key:
            try:
                self.llm = ChatOpenAI(
                    api_key=self.openai_api_key,
                    model="gpt-3.5-turbo",
                    temperature=0.7
                )
                
                self.tools = get_site_generator_tools()
                self.memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
                
                self.agent = initialize_agent(
                    tools=self.tools,
                    llm=self.llm,
                    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                    memory=self.memory,
                    verbose=True
                )
                
                print("✅ Site Generator initialized with AI capabilities")
                
            except Exception as e:
                print(f"Warning: AI initialization failed: {e}")
                print("Falling back to mock mode")
                self.use_mock = True
        else:
            self.use_mock = True
            print("🔧 Site Generator running in mock mode")
    
    def generate_website(self, product_name: str) -> Dict[str, Any]:
        """Generate a complete website from a product name"""
        
        if self.use_mock:
            return self._generate_mock_website(product_name)
        
        try:
            # Step 1: Analyze product
            analysis_prompt = f"Analyze the product '{product_name}' using the product_analyzer tool"
            analysis_result = self.agent.run(analysis_prompt)
            
            # Step 2: Generate content
            content_prompt = f"Generate website content based on this analysis: {analysis_result}"
            content_result = self.agent.run(content_prompt)
            
            # Step 3: Generate HTML
            html_prompt = f"Generate HTML website based on this content: {content_result}"
            html_result = self.agent.run(html_prompt)
            
            # Step 4: Generate images
            image_prompt = f"Generate image specifications based on this analysis: {analysis_result}"
            image_result = self.agent.run(image_prompt)
            
            return {
                "success": True,
                "product_name": product_name,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis_result,
                "content": content_result,
                "html": html_result,
                "images": image_result,
                "generation_method": "AI-powered"
            }
            
        except Exception as e:
            print(f"Error in AI generation: {e}")
            print("Falling back to mock generation")
            return self._generate_mock_website(product_name)
    
    def _generate_mock_website(self, product_name: str) -> Dict[str, Any]:
        """Generate a website using mock tools (for demo/testing)"""
        
        try:
            # Import tools directly
            from site_generator_tools import (
                ProductAnalysisTool, 
                ContentGeneratorTool, 
                HTMLGeneratorTool, 
                ImageGeneratorTool
            )
            
            # Initialize tools
            analyzer = ProductAnalysisTool()
            content_gen = ContentGeneratorTool()
            html_gen = HTMLGeneratorTool()
            image_gen = ImageGeneratorTool()
            
            # Step 1: Analyze product
            print(f"🔍 Analyzing product: {product_name}")
            analysis = analyzer._run(product_name)
            
            # Step 2: Generate content
            print(f"📝 Generating content for: {product_name}")
            content = content_gen._run(analysis)
            
            # Step 3: Generate HTML
            print(f"🎨 Creating HTML website for: {product_name}")
            html = html_gen._run(content)
            
            # Step 4: Generate images
            print(f"🖼️ Generating image specifications for: {product_name}")
            images = image_gen._run(analysis)
            
            return {
                "success": True,
                "product_name": product_name,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis,
                "content": content, 
                "html": html,
                "images": images,
                "generation_method": "Mock tools (demo mode)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "product_name": product_name,
                "timestamp": datetime.now().isoformat()
            }
    
    def save_website(self, result: Dict[str, Any], output_dir: str = "generated_sites") -> str:
        """Save generated website to files"""
        
        if not result.get("success"):
            raise Exception(f"Cannot save failed generation: {result.get('error')}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create site-specific directory
        product_name = result["product_name"]
        safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        site_dir = os.path.join(output_dir, safe_name)
        os.makedirs(site_dir, exist_ok=True)
        
        # Extract HTML from result
        html_content = result.get("html", "")
        if "Generated HTML Website:" in html_content:
            html_content = html_content.split("Generated HTML Website:\n\n")[1]
        
        # Save HTML file
        html_file = os.path.join(site_dir, "index.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save metadata
        metadata = {
            "product_name": result["product_name"],
            "timestamp": result["timestamp"],
            "generation_method": result.get("generation_method"),
            "analysis": result.get("analysis"),
            "content": result.get("content"),
            "images": result.get("images")
        }
        
        metadata_file = os.path.join(site_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return site_dir
    
    def quick_generate(self, product_name: str, save_to_disk: bool = True) -> Dict[str, Any]:
        """Quick one-line generation and save"""
        
        print(f"🚀 Generating website for: {product_name}")
        result = self.generate_website(product_name)
        
        if result.get("success") and save_to_disk:
            try:
                site_dir = self.save_website(result)
                result["saved_to"] = site_dir
                print(f"✅ Website saved to: {site_dir}")
                print(f"🌐 Open {os.path.join(site_dir, 'index.html')} in browser")
            except Exception as e:
                print(f"❌ Error saving website: {e}")
                result["save_error"] = str(e)
        
        return result


def demo_site_generator():
    """Demo the site generator"""
    
    # Test products
    test_products = [
        "EcoSmart Water Bottle",
        "ProCode IDE", 
        "FreshBite Restaurant",
        "FitTracker Pro",
        "StyleHub Fashion"
    ]
    
    generator = OneClickSiteGenerator(use_mock=True)
    
    print("🎯 ONE-CLICK SITE GENERATOR DEMO")
    print("=" * 50)
    
    for product in test_products:
        print(f"\n🔥 Generating site for: {product}")
        result = generator.quick_generate(product, save_to_disk=True)
        
        if result.get("success"):
            print(f"✅ Success! Site generated using {result.get('generation_method')}")
            if result.get("saved_to"):
                print(f"📁 Saved to: {result['saved_to']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
        
        print("-" * 30)


if __name__ == "__main__":
    demo_site_generator() 