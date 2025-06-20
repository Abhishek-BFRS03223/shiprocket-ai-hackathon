#!/usr/bin/env python3
"""
Fixed Hugging Face Image Generator
Uses working models and proper API endpoints
"""

import os
import sys
import requests
import time
from datetime import datetime

class HuggingFaceImageGenerator:
    def __init__(self):
        """Initialize with working HF models"""
        self.token = os.getenv('HUGGINGFACE_TOKEN', '')
        if not self.token:
            print("❌ HUGGINGFACE_TOKEN not found in environment")
            return
        
        # Working models as of 2024
        self.models = [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "runwayml/stable-diffusion-v1-5", 
            "CompVis/stable-diffusion-v1-4",
            "stabilityai/stable-diffusion-2-1"
        ]
        
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def test_model(self, model_name: str) -> bool:
        """Test if model is available and working"""
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Simple test prompt
            response = requests.post(
                url, 
                headers=headers, 
                json={"inputs": "a beautiful sunset"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ {model_name} is working")
                return True
            elif response.status_code == 503:
                print(f"🔄 {model_name} is loading (this is normal)")
                return True
            else:
                print(f"❌ {model_name} failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ {model_name} error: {str(e)}")
            return False
    
    def find_working_model(self) -> str:
        """Find the first working model"""
        print("🔍 Testing Hugging Face models...")
        
        for model in self.models:
            if self.test_model(model):
                print(f"🎯 Using model: {model}")
                return model
        
        print("❌ No working models found")
        return None
    
    def generate_image(self, prompt: str, model: str = None) -> bool:
        """Generate image with working model"""
        if not self.token:
            print("❌ No Hugging Face token")
            return False
        
        if not model:
            model = self.find_working_model()
            if not model:
                return False
        
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Simplified payload that works
        payload = {
            "inputs": prompt[:200],  # Limit prompt length
            "options": {"wait_for_model": True}
        }
        
        try:
            print(f"🎨 Generating: {prompt[:50]}...")
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                # Save image
                timestamp = int(time.time())
                filename = f"hf_image_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                print(f"✅ Image saved: {filepath}")
                return True
                
            elif response.status_code == 503:
                print("🔄 Model loading, waiting...")
                time.sleep(20)
                
                # Retry once
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                if response.status_code == 200:
                    timestamp = int(time.time())
                    filename = f"hf_image_{timestamp}.png"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    
                    print(f"✅ Image saved: {filepath}")
                    return True
                else:
                    print(f"❌ Still failing: {response.status_code}")
                    return False
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

def main():
    """Test the fixed HF generator"""
    print("🧪 TESTING FIXED HUGGING FACE IMAGE GENERATOR")
    print("=" * 50)
    
    generator = HuggingFaceImageGenerator()
    
    if not generator.token:
        print("❌ Please set HUGGINGFACE_TOKEN environment variable")
        print("Get your token from: https://huggingface.co/settings/tokens")
        return
    
    # Test prompts
    test_prompts = [
        "a beautiful landscape",
        "a modern smartphone",
        "a cup of coffee"
    ]
    
    # Find working model
    working_model = generator.find_working_model()
    
    if working_model:
        print(f"\n🎨 Testing image generation with {working_model}")
        
        for prompt in test_prompts:
            success = generator.generate_image(prompt, working_model)
            if success:
                print(f"✅ Generated image for: {prompt}")
                break
            else:
                print(f"❌ Failed to generate: {prompt}")
    
    print("\n🎯 SUMMARY:")
    print("- Use this script instead of the broken one")
    print("- Models tested for compatibility")
    print("- Proper error handling and retries")

if __name__ == "__main__":
    main() 