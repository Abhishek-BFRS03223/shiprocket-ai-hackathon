#!/usr/bin/env python3
"""
AI Image Generator for Product Websites
Generates custom images using DALL-E, Stability AI, or Hugging Face APIs
"""

import os
import sys
import json
import time
import random
import requests
import base64
from datetime import datetime
from typing import Dict, List, Optional

class AIImageGenerator:
    def __init__(self):
        """Initialize AI Image Generator with multiple API support"""
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # API Keys (you'll need to set these)
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.stability_api_key = os.getenv('STABILITY_API_KEY', '')
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN', '')
        
        # Image generation themes
        self.themes = {
            'technology': {
                'styles': ['futuristic', 'sleek modern', 'minimalist tech', 'cyberpunk', 'professional studio'],
                'environments': ['clean white background', 'modern office setting', 'futuristic lab', 'tech workspace', 'gradient backdrop'],
                'lighting': ['studio lighting', 'LED accent lighting', 'soft ambient glow', 'dramatic tech lighting', 'natural daylight']
            },
            'food_beverage': {
                'styles': ['appetizing commercial', 'rustic artisan', 'modern culinary', 'cozy restaurant', 'gourmet presentation'],
                'environments': ['marble countertop', 'wooden table setting', 'restaurant kitchen', 'cafe atmosphere', 'outdoor dining'],
                'lighting': ['warm golden lighting', 'soft natural light', 'dramatic food photography', 'cozy ambient lighting', 'bright daylight']
            },
            'fashion': {
                'styles': ['high fashion editorial', 'street style casual', 'luxury boutique', 'trendy modern', 'classic elegant'],
                'environments': ['fashion studio backdrop', 'urban street scene', 'luxury boutique', 'minimalist setting', 'artistic backdrop'],
                'lighting': ['professional fashion lighting', 'natural portrait lighting', 'dramatic fashion photography', 'soft beauty lighting', 'editorial lighting']
            },
            'health_wellness': {
                'styles': ['clean wellness aesthetic', 'natural organic', 'medical professional', 'fitness focused', 'spa luxury'],
                'environments': ['clean medical setting', 'natural outdoor environment', 'modern gym', 'spa atmosphere', 'wellness center'],
                'lighting': ['clean bright lighting', 'soft natural lighting', 'professional medical lighting', 'warm wellness lighting', 'energizing daylight']
            },
            'business': {
                'styles': ['corporate professional', 'modern business', 'executive luxury', 'startup innovative', 'consulting expert'],
                'environments': ['modern office', 'conference room', 'executive suite', 'business center', 'corporate lobby'],
                'lighting': ['professional office lighting', 'executive lighting', 'modern business lighting', 'confident lighting', 'corporate ambiance']
            }
        }
        
        # Image types for different sections
        self.image_types = {
            'hero_background': {
                'size': '1920x1080',
                'description': 'wide panoramic background image',
                'style_modifier': 'cinematic wide shot'
            },
            'product_showcase': {
                'size': '800x600',
                'description': 'product focused image',
                'style_modifier': 'product photography'
            },
            'feature_icon': {
                'size': '400x400',
                'description': 'feature illustration',
                'style_modifier': 'icon style graphic'
            },
            'gallery_item': {
                'size': '600x400',
                'description': 'lifestyle image',
                'style_modifier': 'lifestyle photography'
            }
        }

    def categorize_product(self, product_name: str) -> str:
        """Categorize product to determine theme"""
        product_lower = product_name.lower()
        
        # Technology keywords
        tech_keywords = ['smart', 'ai', 'tech', 'app', 'software', 'digital', 'robot', 'drone', 'gadget', 'device', 'electronic', 'computer', 'mobile', 'laptop', 'camera', 'headphone', 'speaker', 'watch']
        
        # Food & Beverage keywords
        food_keywords = ['food', 'drink', 'coffee', 'tea', 'restaurant', 'cafe', 'kitchen', 'recipe', 'meal', 'pizza', 'burger', 'cake', 'wine', 'beer', 'juice', 'bakery']
        
        # Fashion keywords
        fashion_keywords = ['fashion', 'clothing', 'style', 'dress', 'shirt', 'pants', 'shoes', 'bag', 'accessory', 'jewelry', 'boutique', 'designer', 'apparel']
        
        # Health & Wellness keywords
        health_keywords = ['health', 'wellness', 'fitness', 'yoga', 'gym', 'medical', 'therapy', 'nutrition', 'vitamin', 'supplement', 'exercise', 'workout', 'spa']
        
        # Business keywords
        business_keywords = ['business', 'corporate', 'company', 'service', 'consulting', 'professional', 'office', 'team', 'solution', 'agency', 'marketing']
        
        for keyword in tech_keywords:
            if keyword in product_lower:
                return 'technology'
        
        for keyword in food_keywords:
            if keyword in product_lower:
                return 'food_beverage'
                
        for keyword in fashion_keywords:
            if keyword in product_lower:
                return 'fashion'
                
        for keyword in health_keywords:
            if keyword in product_lower:
                return 'health_wellness'
                
        for keyword in business_keywords:
            if keyword in product_lower:
                return 'business'
        
        return 'technology'  # default

    def generate_prompt(self, product_name: str, image_type: str, theme: str, variation: int = 0) -> str:
        """Generate detailed AI prompt for image generation"""
        theme_data = self.themes.get(theme, self.themes['technology'])
        image_config = self.image_types.get(image_type, self.image_types['product_showcase'])
        
        # Select style based on variation to ensure diversity
        style = theme_data['styles'][variation % len(theme_data['styles'])]
        environment = theme_data['environments'][variation % len(theme_data['environments'])]
        lighting = theme_data['lighting'][variation % len(theme_data['lighting'])]
        
        # Base prompt construction
        if image_type == 'hero_background':
            prompt = f"Professional {style} {image_config['description']} featuring {product_name}, {environment}, {lighting}, {image_config['style_modifier']}, high quality, detailed, commercial photography"
        elif image_type == 'product_showcase':
            prompt = f"{style} {image_config['style_modifier']} of {product_name}, {environment}, {lighting}, professional commercial quality, detailed, sharp focus"
        elif image_type == 'feature_icon':
            prompt = f"Modern {image_config['style_modifier']} representing {product_name} features, {style} design, clean, professional, {lighting}"
        else:  # gallery_item
            prompt = f"{style} {image_config['style_modifier']} showing {product_name} in use, {environment}, {lighting}, realistic, high quality"
        
        # Add quality modifiers
        prompt += ", 8K resolution, professional photography, commercial quality, detailed, vibrant colors"
        
        return prompt

    def generate_with_openai_dalle(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """Generate image using OpenAI DALL-E 3"""
        if not self.openai_api_key:
            print("❌ OpenAI API key not provided")
            return None
            
        try:
            print(f"🎨 Generating with DALL-E 3: {prompt[:100]}...")
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Map size to DALL-E supported sizes
            dalle_size = "1024x1024"  # DALL-E 3 default
            if "1920" in size or "1080" in size:
                dalle_size = "1792x1024"  # Wide format
            elif "400" in size:
                dalle_size = "1024x1024"  # Square format
            
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": dalle_size,
                "quality": "hd",
                "style": "vivid"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                print("✅ DALL-E 3 generation successful")
                return image_url
            else:
                print(f"❌ DALL-E 3 error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ DALL-E 3 generation failed: {str(e)}")
            return None

    def generate_with_stability_ai(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """Generate image using Stability AI"""
        if not self.stability_api_key:
            print("❌ Stability AI API key not provided")
            return None
            
        try:
            print(f"🎨 Generating with Stability AI: {prompt[:100]}...")
            
            # Map size to Stability AI dimensions
            width, height = 1024, 1024
            if "1920" in size:
                width, height = 1536, 864  # 16:9 ratio
            elif "800" in size:
                width, height = 1024, 768
            elif "400" in size:
                width, height = 1024, 1024
            elif "600" in size:
                width, height = 1024, 768
            
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.stability_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": 30,
                "style_preset": "photographic"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                # Save base64 image to file
                image_data = result['artifacts'][0]['base64']
                timestamp = int(time.time())
                filename = f"stability_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(image_data))
                
                print("✅ Stability AI generation successful")
                return filepath
            else:
                print(f"❌ Stability AI error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Stability AI generation failed: {str(e)}")
            return None

    def generate_with_huggingface(self, prompt, width=512, height=512):
        """Generate image using Hugging Face free API with simpler model"""
        token = self.huggingface_token
        if not token:
            raise Exception("HUGGINGFACE_TOKEN not found in environment")
        
        # Use a more reliable free model
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Simplify the payload for better compatibility
        payload = {
            "inputs": prompt[:500],  # Limit prompt length
            "parameters": {
                "num_inference_steps": 20,  # Reduce for faster generation
                "guidance_scale": 7.5
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 503:
                # Model loading, wait and retry
                print("🔄 Model loading, waiting 10 seconds...")
                time.sleep(10)
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)
                if response.status_code == 200:
                    return response.content
            
            # If still failing, try an even simpler model
            if response.status_code != 200:
                # Fallback to a simpler model
                api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                simple_payload = {"inputs": prompt[:200]}
                
                response = requests.post(api_url, headers=headers, json=simple_payload, timeout=60)
                if response.status_code == 200:
                    return response.content
            
            raise Exception(f"{response.status_code} - {response.text}")
            
        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}")

    def download_image(self, url: str, filename: str) -> Optional[str]:
        """Download image from URL and save locally"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
            return None
        except Exception as e:
            print(f"❌ Image download failed: {str(e)}")
            return None

    def generate_product_images(self, product_name: str, api_preference: str = "auto") -> Dict[str, List[str]]:
        """Generate complete set of images for a product"""
        print(f"🎯 Generating AI images for: {product_name}")
        
        # Categorize product
        category = self.categorize_product(product_name)
        print(f"📂 Category: {category}")
        
        generated_images = {
            'hero_background': [],
            'product_showcase': [],
            'feature_icons': [],
            'gallery_items': []
        }
        
        # Generate different types of images
        image_configs = [
            ('hero_background', 1),  # 1 hero image
            ('product_showcase', 2), # 2 product showcase images
            ('feature_icon', 3),     # 3 feature icons
            ('gallery_item', 4)      # 4 gallery images
        ]
        
        for image_type, count in image_configs:
            print(f"\n🎨 Generating {count} {image_type} images...")
            
            for i in range(count):
                # Generate unique prompt for variation
                prompt = self.generate_prompt(product_name, image_type, category, i)
                size = self.image_types[image_type]['size']
                
                # Try different APIs based on preference
                image_path = None
                
                if api_preference == "dalle" or api_preference == "auto":
                    image_url = self.generate_with_openai_dalle(prompt, size)
                    if image_url:
                        filename = f"{product_name.replace(' ', '_').lower()}_{image_type}_{i+1}_{int(time.time())}.png"
                        image_path = self.download_image(image_url, filename)
                
                if not image_path and (api_preference == "stability" or api_preference == "auto"):
                    image_path = self.generate_with_stability_ai(prompt, size)
                
                if not image_path and (api_preference == "huggingface" or api_preference == "auto"):
                    try:
                        image_content = self.generate_with_huggingface(prompt)
                        if image_content:
                            # Save the image
                            timestamp = int(time.time())
                            filename = f"huggingface_{image_type}_{i}_{timestamp}.png"
                            filepath = os.path.join(self.output_dir, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(image_content)
                            
                            print("✅ Hugging Face generation successful")
                            image_path = filepath
                    except Exception as e:
                        print(f"❌ Hugging Face error: {str(e)}")
                
                if image_path:
                    if image_type == 'feature_icon':
                        generated_images['feature_icons'].append(image_path)
                    elif image_type == 'gallery_item':
                        generated_images['gallery_items'].append(image_path)
                    else:
                        generated_images[image_type].append(image_path)
                    print(f"✅ Generated: {image_path}")
                else:
                    print(f"❌ Failed to generate {image_type} #{i+1}")
                
                # Small delay to respect API limits
                time.sleep(1)
        
        return generated_images

    def generate_for_website(self, product_name: str, api_preference: str = "auto") -> Dict:
        """Generate images and return data for website integration"""
        images = self.generate_product_images(product_name, api_preference)
        
        # Convert local paths to web-accessible URLs
        web_images = {}
        for image_type, paths in images.items():
            web_images[image_type] = []
            for path in paths:
                # Convert to relative web path
                web_path = path.replace(self.output_dir, '/generated_images')
                web_images[image_type].append(web_path)
        
        return {
            'success': True,
            'product_name': product_name,
            'category': self.categorize_product(product_name),
            'images': web_images,
            'generated_at': datetime.now().isoformat(),
            'total_images': sum(len(paths) for paths in images.values())
        }

def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python ai_image_generator.py <product_name> [api_preference]")
        print("API preferences: dalle, stability, huggingface, auto")
        return
    
    product_name = ' '.join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
    api_preference = sys.argv[-1] if len(sys.argv) > 2 else "auto"
    
    generator = AIImageGenerator()
    
    try:
        result = generator.generate_for_website(product_name, api_preference)
        if result['success']:
            print(f"\n🎉 SUCCESS: Generated {result['total_images']} AI images for {product_name}")
            print(f"📁 Images saved in: {generator.output_dir}")
            print(f"🎯 Category: {result['category']}")
        else:
            print("❌ FAILED: No images were generated")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main() 