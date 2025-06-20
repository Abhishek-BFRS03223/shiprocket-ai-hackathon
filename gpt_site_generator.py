#!/usr/bin/env python3
"""
Enhanced GPT-Powered Dynamic Site Generator
Uses GPT API and Hugging Face API to generate unique themed ecommerce websites
"""

import os
import sys
import json
import requests
import time
import random
import tempfile
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from io import BytesIO
# Try to import PIL, fallback if not available
try:
    from PIL import Image
except ImportError:
    # Fallback for environments without PIL
    Image = None
    print("Warning: PIL not available, using fallback image handling")

# Hugging Face configuration
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
HF_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')

def generate_product_image(prompt: str, retries: int = 3) -> str:
    """Generate product-specific image using ONLY DALL-E API"""
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not openai_api_key or openai_api_key == 'your_openai_key_here':
        print("❌ No valid OpenAI API key - cannot generate images")
        return get_smart_fallback_image(prompt)
    
    try:
        import openai
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Clean and optimize prompt for DALL-E
        clean_prompt = clean_dalle_prompt(prompt)
        print(f"🎨 Generating DALL-E image for: {clean_prompt}")
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=clean_prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            style="vivid"
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"✅ DALL-E image generated successfully")
            return image_url
        else:
            print("❌ No image data returned from DALL-E")
            return get_smart_fallback_image(prompt)
            
    except openai.RateLimitError as e:
        print(f"⚠️ OpenAI quota exceeded - using smart fallback images")
        return get_smart_fallback_image(prompt)
    except openai.BadRequestError as e:
        print(f"⚠️ DALL-E request error (may be content policy) - using smart fallback")
        return get_smart_fallback_image(prompt)
    except Exception as e:
        print(f"❌ DALL-E generation failed: {e}")
        return get_smart_fallback_image(prompt)

def clean_dalle_prompt(prompt: str) -> str:
    """Clean and optimize prompt for DALL-E API"""
    # Remove redundant photography terms that might confuse DALL-E
    prompt = prompt.replace("professional product photo of", "").strip()
    prompt = prompt.replace("studio lighting", "").strip()
    prompt = prompt.replace("commercial photography style", "").strip()
    prompt = prompt.replace("4K resolution", "").strip()
    prompt = prompt.replace("marketing image", "").strip()
    
    # Create a clean, focused prompt
    if not prompt:
        prompt = "product"
    
    # Add back essential context for product images
    clean_prompt = f"A professional product photograph of {prompt}, clean white background, studio lighting, high quality"
    
    # Ensure prompt is within DALL-E limits (under 1000 characters)
    if len(clean_prompt) > 800:
        clean_prompt = f"Professional photo of {prompt}, white background"
    
    return clean_prompt

def extract_key_product_words(prompt: str) -> str:
    """Extract the most important product-related words from a prompt"""
    # Remove common words and focus on product-specific terms
    words = prompt.lower().replace('professional product photo of', '').replace('studio lighting', '').replace('white background', '').replace('commercial photography style', '').replace('detailed', '').replace('4k resolution', '').replace('marketing image', '').strip()
    
    # Split and take first few meaningful words
    key_words = [w for w in words.split() if len(w) > 2 and w not in ['and', 'the', 'for', 'with', 'from']]
    return ' '.join(key_words[:3])  # Take first 3 meaningful words

def get_smart_fallback_image(prompt: str) -> str:
    """Get smart fallback images based on product type detection"""
    prompt_lower = prompt.lower()
    
    # Technology products
    if any(word in prompt_lower for word in ['laptop', 'computer', 'gaming', 'mouse', 'keyboard', 'phone', 'smartphone', 'tablet', 'headphones', 'tech', 'electronic', 'device', 'gadget']):
        tech_images = [
            "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&h=600&fit=crop&q=80",  # Laptop
            "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=600&fit=crop&q=80",  # Gaming setup
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&h=600&fit=crop&q=80",  # Headphones
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=600&fit=crop&q=80",  # Phone
        ]
        return tech_images[hash(prompt) % len(tech_images)]
    
    # Fashion and accessories
    elif any(word in prompt_lower for word in ['fashion', 'clothing', 'accessory', 'bag', 'handbag', 'watch', 'jewelry', 'shoes', 'apparel']):
        fashion_images = [
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=600&fit=crop&q=80",  # Handbag
            "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?w=800&h=600&fit=crop&q=80",  # Watch
            "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&h=600&fit=crop&q=80",  # Shoes
            "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=800&h=600&fit=crop&q=80",  # Fashion
        ]
        return fashion_images[hash(prompt) % len(fashion_images)]
    
    # Food and beverage
    elif any(word in prompt_lower for word in ['coffee', 'food', 'beverage', 'drink', 'kitchen', 'cooking', 'restaurant', 'culinary']):
        food_images = [
            "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&h=600&fit=crop&q=80",  # Coffee
            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop&q=80",  # Kitchen
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800&h=600&fit=crop&q=80",  # Food
            "https://images.unsplash.com/photo-1555126634-323283e090fa?w=800&h=600&fit=crop&q=80",  # Beverage
        ]
        return food_images[hash(prompt) % len(food_images)]
    
    # Health and wellness
    elif any(word in prompt_lower for word in ['health', 'fitness', 'wellness', 'medical', 'yoga', 'exercise', 'supplement', 'beauty']):
        health_images = [
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop&q=80",  # Yoga
            "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop&q=80",  # Fitness
            "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=600&fit=crop&q=80",  # Wellness
            "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&h=600&fit=crop&q=80",  # Health
        ]
        return health_images[hash(prompt) % len(health_images)]
    
    # Default to a professional product display
    return "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop&q=80"

def get_pexels_image(search_term, size="large2x"):
    """REMOVED: Pexels support removed as requested - using DALL-E only"""
    # This function is kept for compatibility but always returns None
    # to trigger DALL-E generation
    return None

class EnhancedGPTSiteGenerator:
    def __init__(self):
        """Initialize Enhanced GPT Site Generator"""
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        if not self.api_key:
            print("⚠️ No OpenAI API key found. Using enhanced fallback mode.")
        else:
            # Initialize OpenAI client
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            print("✅ OpenAI client initialized successfully")
        
        # Use temporary directory for non-persistent storage
        self.temp_dir = tempfile.mkdtemp(prefix="temp_sites_")
        
        # Enhanced theme system
        self.themes = {
            "modern_minimal": {
                "name": "Modern Minimal",
                "primary": "#1a1a1a",
                "secondary": "#f8f9fa", 
                "accent": "#007bff",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Inter', 'Segoe UI', sans-serif",
                "border_radius": "12px",
                "shadow": "0 8px 32px rgba(0,0,0,0.1)"
            },
            "vibrant_modern": {
                "name": "Vibrant Modern",
                "primary": "#6c5ce7",
                "secondary": "#a29bfe",
                "accent": "#fd79a8", 
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Poppins', sans-serif",
                "border_radius": "20px",
                "shadow": "0 15px 35px rgba(108, 92, 231, 0.2)"
            },
            "luxury_elegant": {
                "name": "Luxury Elegant",
                "primary": "#2d3436",
                "secondary": "#ddd6fe",
                "accent": "#d4af37",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Playfair Display', serif",
                "border_radius": "8px",
                "shadow": "0 10px 40px rgba(212, 175, 55, 0.2)"
            },
            "tech_futuristic": {
                "name": "Tech Futuristic", 
                "primary": "#0984e3",
                "secondary": "#74b9ff",
                "accent": "#00cec9",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Roboto', sans-serif",
                "border_radius": "4px",
                "shadow": "0 8px 25px rgba(9, 132, 227, 0.3)"
            },
            "organic_natural": {
                "name": "Organic Natural",
                "primary": "#27ae60",
                "secondary": "#55a3ff",
                "accent": "#f39c12",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Nunito', sans-serif",
                "border_radius": "25px",
                "shadow": "0 12px 28px rgba(39, 174, 96, 0.2)"
            },
            "dark_premium": {
                "name": "Dark Premium",
                "primary": "#2c3e50",
                "secondary": "#34495e",
                "accent": "#e74c3c",
                "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "font_family": "'Montserrat', sans-serif",
                "border_radius": "10px",
                "shadow": "0 20px 40px rgba(0,0,0,0.3)"
            }
        }
    
    def categorize_product(self, product_name: str) -> str:
        """Enhanced product categorization with GPT"""
        if not self.api_key:
            return self._fallback_categorization(product_name)
        
        try:
            prompt = f"""
            Analyze this product and categorize it into ONE of these specific categories:
            - technology (gadgets, electronics, software, AI, smart devices)
            - fashion (clothing, accessories, jewelry, bags, shoes)
            - food_beverage (food, drinks, restaurants, culinary)
            - health_wellness (fitness, medical, beauty, supplements)
            - home_lifestyle (furniture, decor, appliances, tools)
            - automotive (cars, bikes, vehicle accessories)
            - sports_recreation (sports equipment, outdoor gear, games)
            - business_professional (B2B services, office supplies, consulting)
            
            Product: "{product_name}"
            
            Return ONLY the category name (one word with underscore).
            """
            
            response = self._call_openai_api(prompt, max_tokens=20)
            if response:
                category = response.strip().lower()
                valid_categories = [
                    "technology", "fashion", "food_beverage", "health_wellness",
                    "home_lifestyle", "automotive", "sports_recreation", "business_professional"
                ]
                return category if category in valid_categories else "technology"
            
        except Exception as e:
            print(f"GPT categorization failed: {e}")
        
        return self._fallback_categorization(product_name)
    
    def _fallback_categorization(self, product_name: str) -> str:
        """Enhanced fallback categorization with better keyword matching"""
        product_lower = product_name.lower()
        
        # Food & Beverage keywords (check this first for better accuracy)
        if any(word in product_lower for word in [
            'food', 'coffee', 'restaurant', 'bakery', 'pizza', 'organic', 
            'drink', 'beverage', 'recipe', 'meal', 'gourmet', 'artisan',
            'apple', 'fruit', 'vegetable', 'fresh', 'farm', 'beans', 'roast',
            'brew', 'tea', 'wine', 'beer', 'dairy', 'meat', 'seafood', 'spice',
            'sauce', 'soup', 'bread', 'dessert', 'cake', 'cookie', 'chocolate'
        ]):
            return "food_beverage"
            
        # Technology keywords
        elif any(word in product_lower for word in [
            'smart', 'ai', 'tech', 'digital', 'app', 'software', 'device', 
            'phone', 'laptop', 'computer', 'drone', 'robot', 'electronic',
            'gadget', 'virtual', 'augmented', 'machine', 'algorithm', 'data'
        ]):
            return "technology"
        
        # Fashion keywords  
        elif any(word in product_lower for word in [
            'fashion', 'clothing', 'dress', 'shirt', 'shoes', 'bag', 'handbag',
            'jewelry', 'watch', 'style', 'designer', 'luxury', 'saree',
            'pants', 'jacket', 'coat', 'suit', 'tie', 'belt', 'hat', 'scarf'
        ]):
            return "fashion"
        
        # Health & Wellness keywords
        elif any(word in product_lower for word in [
            'health', 'fitness', 'wellness', 'yoga', 'gym', 'medical', 
            'beauty', 'cosmetic', 'care', 'supplement', 'vitamin', 'protein',
            'therapy', 'treatment', 'skincare', 'massage', 'meditation'
        ]):
            return "health_wellness"
        
        # Automotive keywords
        elif any(word in product_lower for word in [
            'car', 'vehicle', 'automotive', 'bike', 'motorcycle', 'truck',
            'engine', 'wheel', 'tire', 'brake', 'motor', 'racing'
        ]):
            return "automotive"
        
        # Sports & Recreation keywords
        elif any(word in product_lower for word in [
            'sport', 'game', 'tennis', 'football', 'outdoor', 'recreation',
            'equipment', 'gear', 'basketball', 'soccer', 'golf', 'swimming'
        ]):
            return "sports_recreation"
        
        # Home & Lifestyle keywords (removed kitchen to avoid conflict)
        elif any(word in product_lower for word in [
            'home', 'furniture', 'decor', 'appliance', 'tool', 'garden',
            'bedroom', 'living', 'chair', 'table', 'lamp', 'cleaning'
        ]):
            return "home_lifestyle"
        
        # Business & Professional keywords
        elif any(word in product_lower for word in [
            'business', 'professional', 'office', 'consulting', 'service',
            'marketing', 'finance', 'legal', 'enterprise', 'corporate'
        ]):
            return "business_professional"
        
        else:
            return "food_beverage"  # Changed default to food_beverage for better variety

    def generate_enhanced_content(self, product_name: str, category: str) -> Dict[str, Any]:
        """Generate completely dynamic content using OpenAI - no restrictions or predefined templates"""
        
        print(f"🤖 Generating completely dynamic content for: {product_name}")
        
        # Try OpenAI first - this should be the primary method
        openai_content = self._generate_openai_content(product_name)
        if openai_content:
            return openai_content
        
        # Only use minimal fallback if OpenAI completely fails
        print("🔄 OpenAI unavailable, generating minimal dynamic fallback")
        return self._generate_minimal_dynamic_content(product_name)

    def _generate_openai_content(self, product_name: str) -> Optional[Dict[str, Any]]:
        """Generate content using OpenAI with no restrictions"""
        if not self.api_key:
            print("⚠️ No OpenAI API key - skipping AI generation")
            return None
        
        try:
            print(f"🤖 Calling OpenAI API for: {product_name}")
            
            # Ultra-dynamic prompt that handles ANY product
            prompt = f"""
            You are an expert e-commerce website creator. A user wants to create a website for "{product_name}".

            No matter what "{product_name}" is - whether it's a physical product, service, digital product, food item, technology, clothing, book, course, app, or anything else - create a professional e-commerce website.

            IMPORTANT: 
            - Do NOT make assumptions about what "{product_name}" is
            - Research and understand the product based on its name
            - Create authentic, realistic content that makes sense for this specific product
            - Generate appropriate related products that would genuinely complement "{product_name}"
            - Use realistic pricing that makes sense for this type of product
            - Make it feel like a real business selling a real product

            Create a complete website structure with:

            Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
            {{
                "hero": {{
                    "headline": "Compelling headline for {product_name}",
                    "subheadline": "Engaging tagline that captures what this product does", 
                    "description": "2-3 sentences explaining what {product_name} is and its main benefit",
                    "cta_button": "Action-oriented button text"
                }},
                "features": {{
                    "title": "Why Choose {product_name}",
                    "items": [
                        {{"icon": "🎯", "title": "Key benefit 1", "description": "Specific advantage of {product_name}"}},
                        {{"icon": "⚡", "title": "Key benefit 2", "description": "Another important feature"}},
                        {{"icon": "💎", "title": "Key benefit 3", "description": "What makes this special"}},
                        {{"icon": "🚀", "title": "Key benefit 4", "description": "Additional value proposition"}},
                        {{"icon": "⭐", "title": "Key benefit 5", "description": "Quality or service benefit"}},
                        {{"icon": "🔥", "title": "Key benefit 6", "description": "Unique selling point"}}
                    ]
                }},
                "how_it_works": {{
                    "title": "How It Works",
                    "steps": [
                        {{"step": 1, "title": "Step 1", "description": "First thing customer does with {product_name}"}},
                        {{"step": 2, "title": "Step 2", "description": "Next step in the process"}},
                        {{"step": 3, "title": "Step 3", "description": "Final outcome or result"}}
                    ]
                }},
                "testimonials": {{
                    "title": "Customer Reviews",
                    "reviews": [
                        {{"name": "Customer name", "role": "Their role/title", "text": "Specific testimonial about {product_name}", "rating": 5}},
                        {{"name": "Another customer", "role": "Their background", "text": "Different perspective on {product_name}", "rating": 5}}
                    ]
                }},
                "catalog": {{
                    "title": "You Might Also Like",
                    "description": "Products that complement {product_name}",
                    "products": [
                        {{"name": "Related product 1", "price": "$XX", "image_prompt": "professional product photo of [describe related product] on white background"}},
                        {{"name": "Related product 2", "price": "$XX", "image_prompt": "professional product photo of [describe related product] on white background"}},
                        {{"name": "Related product 3", "price": "$XX", "image_prompt": "professional product photo of [describe related product] on white background"}},
                        {{"name": "Related product 4", "price": "$XX", "image_prompt": "professional product photo of [describe related product] on white background"}}
                    ]
                }},
                "pricing": {{
                    "title": "Get {product_name} Today",
                    "price": "$XX",
                    "original_price": "$XX",
                    "features": ["What customer gets 1", "What customer gets 2", "What customer gets 3", "Bonus or guarantee"],
                    "cta": "Buy Now",
                    "guarantee": "Money-back guarantee or return policy"
                }},
                "tagline": "Memorable slogan for {product_name}",
                "meta_description": "SEO-friendly description of {product_name} and its benefits"
            }}

            Make this authentic and realistic. Think about what "{product_name}" actually is and create content that would genuinely help someone understand and want to buy it.
            """
            
            response = self._call_openai_api(prompt, max_tokens=3500)
            
            if response:
                try:
                    # Clean and parse the response
                    content = self._parse_openai_response(response, product_name)
                    if content:
                        print(f"✅ Generated dynamic OpenAI content for {product_name}")
                        return content
                except Exception as e:
                    print(f"❌ Failed to parse OpenAI response: {e}")
            
        except Exception as e:
            print(f"❌ OpenAI generation failed: {e}")
        
        return None

    def _parse_openai_response(self, response: str, product_name: str) -> Optional[Dict[str, Any]]:
        """Parse OpenAI response and extract JSON content"""
        try:
            # Clean the response
            content_text = response.strip()
            
            # Remove markdown formatting if present
            if "```json" in content_text:
                start = content_text.find("```json") + 7
                end = content_text.find("```", start)
                content_text = content_text[start:end].strip()
            elif "```" in content_text:
                start = content_text.find("```") + 3
                end = content_text.rfind("```")
                content_text = content_text[start:end].strip()
            
            # Try to parse JSON
            content = json.loads(content_text)
            
            # Validate that we have the required structure
            required_keys = ['hero', 'features', 'how_it_works', 'testimonials', 'catalog', 'pricing']
            if all(key in content for key in required_keys):
                return content
            else:
                print(f"❌ Missing required keys in OpenAI response")
                return None
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            # Try to fix common JSON issues
            try:
                import re
                # Try to extract JSON object
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    content = json.loads(json_match.group())
                    return content
            except:
                pass
        
        return None

    def _generate_minimal_dynamic_content(self, product_name: str) -> Dict[str, Any]:
        """Generate minimal dynamic content when OpenAI is unavailable"""
        import random
        
        print(f"🎨 Creating minimal dynamic content for: {product_name}")
        
        # Extract meaningful words from product name
        words = product_name.lower().split()
        main_word = words[0] if words else "product"
        
        # Generate realistic pricing
        base_price = random.randint(29, 899)
        original_price = base_price + random.randint(20, 200)
        
        # Generate dynamic content that adapts to any product
        content = {
            "hero": {
                "headline": f"Premium {product_name}",
                "subheadline": f"Experience the difference quality makes",
                "description": f"Discover why {product_name} is the smart choice for those who demand excellence. Quality, value, and satisfaction guaranteed.",
                "cta_button": f"Get {product_name}"
            },
            "features": {
                "title": f"Why Choose {product_name}",
                "items": [
                    {"icon": "⭐", "title": "Premium Quality", "description": f"Our {product_name} meets the highest standards of excellence"},
                    {"icon": "🚀", "title": "Fast Results", "description": f"Experience the benefits of {product_name} right away"},
                    {"icon": "💎", "title": "Great Value", "description": f"Get more for your money with our {product_name}"},
                    {"icon": "🛡️", "title": "Reliable Choice", "description": f"Trust in the proven performance of {product_name}"},
                    {"icon": "⚡", "title": "Easy to Use", "description": f"Simple and straightforward - {product_name} just works"},
                    {"icon": "🎯", "title": "Perfect Fit", "description": f"Designed to meet your specific {main_word} needs"}
                ]
            },
            "how_it_works": {
                "title": f"Getting Started with {product_name}",
                "steps": [
                    {"step": 1, "title": "Order", "description": f"Choose your {product_name} and place your order"},
                    {"step": 2, "title": "Receive", "description": f"Get your {product_name} delivered quickly and safely"},
                    {"step": 3, "title": "Enjoy", "description": f"Start enjoying all the benefits of {product_name}"}
                ]
            },
            "testimonials": {
                "title": "Customer Reviews",
                "reviews": [
                    {"name": "Alex Johnson", "role": "Satisfied Customer", "text": f"This {product_name} exceeded my expectations. Highly recommended!", "rating": 5},
                    {"name": "Sarah Chen", "role": "Verified Buyer", "text": f"Amazing quality and great value. My {product_name} is perfect!", "rating": 5}
                ]
            },
            "catalog": {
                "title": "Complete Your Purchase",
                "description": f"Perfect additions to your {product_name}",
                "products": self._generate_dynamic_related_products(product_name, main_word)
            },
            "pricing": {
                "title": f"Get Your {product_name} Today",
                "price": f"${base_price}",
                "original_price": f"${original_price}",
                "features": [
                    f"Complete {product_name}",
                    "Free shipping included",
                    "Customer support",
                    "Satisfaction guarantee"
                ],
                "cta": f"Order {product_name}",
                "guarantee": "30-day satisfaction guarantee"
            },
            "tagline": f"The smart choice for {main_word}",
            "meta_description": f"Get the best {product_name} with premium quality, great value, and guaranteed satisfaction."
        }
        
        return content

    def _generate_dynamic_related_products(self, product_name: str, main_word: str) -> List[Dict]:
        """Generate related products dynamically based on the main product"""
        import random
        
        # Generate generic but relevant accessories
        accessories = [
            f"{main_word.title()} Accessories",
            f"Premium {main_word.title()} Kit",
            f"{main_word.title()} Care Package",
            f"Enhanced {main_word.title()} Bundle"
        ]
        
        related_products = []
        for i, accessory in enumerate(accessories):
            price = random.randint(15, 199)
            related_products.append({
                "name": accessory,
                "price": f"${price}",
                "image_prompt": f"professional product photo of {accessory.lower()} on white background"
            })
        
        return related_products

    def _call_openai_api(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """Make OpenAI API call with improved error handling"""
        if not self.api_key:
            print("⚠️ No OpenAI API key available")
            return None
        
        if not hasattr(self, 'client'):
            print("⚠️ OpenAI client not initialized")
            return None
        
        try:
            print("🔄 Calling OpenAI API...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert e-commerce copywriter and web designer. Create authentic, realistic content for any product the user describes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.8
            )
            
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                if content:
                    print("✅ OpenAI API call successful")
                    return content.strip()
            
            print("❌ Empty response from OpenAI API")
            return None
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ OpenAI API error: {error_str}")
            
            if "quota" in error_str.lower() or "429" in error_str:
                print("💡 API quota exceeded - using dynamic fallback")
            elif "ssl" in error_str.lower() or "certificate" in error_str.lower():
                print("🔒 SSL certificate issue - using dynamic fallback")
            elif "connection" in error_str.lower():
                print("🌐 Connection issue - using dynamic fallback")
            else:
                print("⚠️ Unexpected API error - using dynamic fallback")
            
            return None

    def generate_website(self, product_name: str) -> str:
        """Generate complete enhanced website"""
        print(f"🔍 Analyzing product: {product_name}")
        
        # Step 1: Categorize product
        category = self.categorize_product(product_name)
        print(f"📂 Category detected: {category}")
        
        # Step 2: Select random theme for variety
        theme_key = random.choice(list(self.themes.keys()))
        theme = self.themes[theme_key]
        print(f"🎨 Theme selected: {theme['name']}")
        
        # Step 3: Generate enhanced content
        print(f"📝 Generating enhanced content...")
        content = self.generate_enhanced_content(product_name, category)
        
        # Step 4: Generate HTML with selected theme
        print(f"🌐 Building themed website...")
        html = self.generate_themed_html(product_name, content, category, theme)
        
        # Step 5: Create temporary file (non-persistent)
        import uuid
        site_id = str(uuid.uuid4())[:8]
        site_file = os.path.join(self.temp_dir, f"{site_id}.html")
        
        with open(site_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Enhanced themed website generated successfully!")
        return site_file

    def generate_themed_html(self, product_name: str, content: Dict, category: str, theme: Dict) -> str:
        """Generate HTML with dynamic themes and enhanced ecommerce features"""
        
        # Get high-quality hero background using DALL-E
        hero_bg = generate_product_image(f"{product_name} hero background")
        
        # Generate product catalog images
        catalog_html = ""
        if 'catalog' in content:
            for product in content['catalog']['products']:
                img_url = generate_product_image(product['image_prompt'])
                catalog_html += f'''
                <div class="product-card">
                    <img src="{img_url}" alt="{product['name']}" loading="lazy">
                    <h3>{product['name']}</h3>
                    <div class="price">{product['price']}</div>
                    <button class="product-cta">Add to Cart</button>
                </div>'''
        
        # Enhanced HTML with modern design and ecommerce features
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name} - {content['tagline']}</title>
    <meta name="description" content="{content['meta_description']}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&family=Nunito:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --text-color: #2c3e50;
            --gradient: {theme['gradient']};
            --font-family: {theme['font_family']};
            --border-radius: {theme['border_radius']};
            --shadow: {theme['shadow']};
        }}
        
        body {{ 
            font-family: var(--font-family); 
            line-height: 1.7; 
            color: var(--text-color);
            overflow-x: hidden;
        }}
        
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 0 20px; 
        }}
        
        /* Header */
        .header {{ 
            background: var(--primary-color); 
            color: white; 
            padding: 1rem 0; 
            position: fixed; 
            width: 100%; 
            top: 0; 
            z-index: 1000;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
        }}
        
        .nav {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }}
        
        .logo {{ 
            font-size: 1.8rem; 
            font-weight: 700; 
            color: white; 
            text-decoration: none;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .nav-links {{ 
            display: flex; 
            list-style: none; 
            gap: 2.5rem; 
        }}
        
        .nav-links a {{ 
            color: white; 
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .nav-links a:hover {{
            color: var(--accent-color);
            transform: translateY(-2px);
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.4)), url('{hero_bg}');
            background-size: cover; 
            background-position: center; 
            background-attachment: fixed;
            height: 100vh;
            display: flex; 
            align-items: center; 
            color: white; 
            text-align: center;
            position: relative;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--gradient);
            opacity: 0.1;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
        }}
        
        .hero h1 {{ 
            font-size: 4rem; 
            margin-bottom: 1.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: fadeInUp 1s ease-out;
        }}
        
        .hero p {{ 
            font-size: 1.4rem; 
            margin-bottom: 2.5rem; 
            max-width: 600px; 
            margin-left: auto; 
            margin-right: auto;
            opacity: 0.95;
            animation: fadeInUp 1s ease-out 0.3s both;
        }}
        
        .cta-button {{
            background: var(--gradient);
            color: white; 
            padding: 18px 40px;
            text-decoration: none; 
            border-radius: var(--border-radius);
            font-weight: 600;
            font-size: 1.1rem;
            display: inline-block; 
            transition: all 0.4s ease;
            box-shadow: var(--shadow);
            border: none;
            cursor: pointer;
            animation: fadeInUp 1s ease-out 0.6s both;
        }}
        
        .cta-button:hover {{ 
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }}
        
        /* Sections */
        .section {{ 
            padding: 100px 0; 
            position: relative;
        }}
        
        .section:nth-child(even) {{
            background: linear-gradient(135deg, var(--secondary-color), #ffffff);
        }}
        
        .section-title {{ 
            text-align: center; 
            font-size: 3rem; 
            margin-bottom: 4rem; 
            color: var(--primary-color);
            font-weight: 600;
            position: relative;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: var(--gradient);
            border-radius: 2px;
        }}
        
        /* Features Grid */
        .features-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 3rem; 
        }}
        
        .feature-card {{ 
            background: white; 
            padding: 3rem 2rem; 
            border-radius: var(--border-radius);
            text-align: center; 
            box-shadow: var(--shadow);
            transition: all 0.4s ease;
            border: 1px solid rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }}
        
        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient);
        }}
        
        .feature-card:hover {{ 
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }}
        
        .feature-icon {{ 
            font-size: 4rem; 
            margin-bottom: 1.5rem;
            display: block;
        }}
        
        .feature-card h3 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        .feature-card p {{
            color: #666;
            line-height: 1.6;
        }}
        
        /* Steps */
        .steps {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 3rem; 
        }}
        
        .step {{ 
            text-align: center; 
            padding: 2.5rem;
            position: relative;
        }}
        
        .step-number {{
            background: var(--gradient);
            color: white; 
            width: 80px; 
            height: 80px;
            border-radius: 50%; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            font-size: 2rem; 
            font-weight: 700; 
            margin: 0 auto 2rem;
            box-shadow: var(--shadow);
        }}
        
        .step h3 {{
            font-size: 1.4rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        /* Product Catalog */
        .catalog-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2.5rem;
            margin-top: 3rem;
        }}
        
        .product-card {{
            background: white;
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: all 0.4s ease;
            position: relative;
        }}
        
        .product-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }}
        
        .product-card img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
        }}
        
        .product-card h3 {{
            padding: 1.5rem 1.5rem 0.5rem;
            font-size: 1.3rem;
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        .product-card .price {{
            padding: 0 1.5rem;
            font-size: 1.5rem;
            color: var(--accent-color);
            font-weight: 700;
        }}
        
        .product-cta {{
            width: 100%;
            padding: 1rem;
            background: var(--gradient);
            color: white;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .product-cta:hover {{
            background: var(--primary-color);
        }}
        
        /* Testimonials */
        .testimonials {{ 
            background: linear-gradient(135deg, var(--secondary-color), #f8f9fa);
        }}
        
        .testimonials-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 3rem; 
        }}
        
        .testimonial {{ 
            background: white; 
            padding: 3rem; 
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            position: relative;
            border-left: 5px solid var(--accent-color);
        }}
        
        .testimonial::before {{
            content: '"';
            position: absolute;
            top: -10px;
            left: 20px;
            font-size: 4rem;
            color: var(--accent-color);
            font-family: serif;
        }}
        
        /* Pricing */
        .pricing {{ 
            background: var(--gradient);
            color: white; 
            text-align: center; 
        }}
        
        .pricing-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: var(--border-radius);
            padding: 4rem 3rem;
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .price {{ 
            font-size: 4rem; 
            font-weight: 700; 
            margin: 1.5rem 0;
            position: relative;
        }}
        
        .original-price {{
            font-size: 1.5rem;
            text-decoration: line-through;
            opacity: 0.7;
            margin-bottom: 0.5rem;
        }}
        
        .pricing-features {{ 
            list-style: none; 
            margin: 3rem 0;
            text-align: left;
        }}
        
        .pricing-features li {{ 
            padding: 0.8rem 0;
            position: relative;
            padding-left: 2rem;
        }}
        
        .pricing-features li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--accent-color);
            font-weight: bold;
        }}
        
        /* Footer */
        .footer {{ 
            background: var(--text-color);
            color: white; 
            text-align: center; 
            padding: 4rem 0;
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2.5rem; }}
            .nav-links {{ display: none; }}
            .section {{ padding: 60px 0; }}
            .features-grid {{ grid-template-columns: 1fr; }}
            .catalog-grid {{ grid-template-columns: 1fr; }}
            .testimonials-grid {{ grid-template-columns: 1fr; }}
        }}
        
        @media (max-width: 480px) {{
            .hero h1 {{ font-size: 2rem; }}
            .hero p {{ font-size: 1.1rem; }}
            .section-title {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="#" class="logo">{product_name}</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#catalog">Products</a></li>
                <li><a href="#testimonials">Reviews</a></li>
                <li><a href="#pricing">Pricing</a></li>
            </ul>
        </nav>
    </header>

    <section id="home" class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>{content['hero']['headline']}</h1>
                <p>{content['hero']['description']}</p>
                <a href="#pricing" class="cta-button">{content['hero']['cta_button']}</a>
            </div>
        </div>
    </section>

    <section id="features" class="section">
        <div class="container">
            <h2 class="section-title">{content['features']['title']}</h2>
            <div class="features-grid">'''
        
        # Add enhanced feature cards
        for item in content['features']['items']:
            html += f'''
                <div class="feature-card">
                    <div class="feature-icon">{item['icon']}</div>
                    <h3>{item['title']}</h3>
                    <p>{item['description']}</p>
                </div>'''
        
        html += f'''
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <h2 class="section-title">{content['how_it_works']['title']}</h2>
            <div class="steps">'''
        
        for step in content['how_it_works']['steps']:
            html += f'''
                <div class="step">
                    <div class="step-number">{step['step']}</div>
                    <h3>{step['title']}</h3>
                    <p>{step['description']}</p>
                </div>'''
        
        # Add product catalog section if available
        if 'catalog' in content:
            html += f'''
            </div>
        </div>
    </section>

    <section id="catalog" class="section">
        <div class="container">
            <h2 class="section-title">{content['catalog']['title']}</h2>
            <p style="text-align: center; font-size: 1.2rem; margin-bottom: 3rem; color: #666;">{content['catalog']['description']}</p>
            <div class="catalog-grid">
                {catalog_html}
            </div>
        </div>
    </section>'''
        else:
            html += '''
            </div>
        </div>
    </section>'''

        html += f'''
    <section id="testimonials" class="section testimonials">
        <div class="container">
            <h2 class="section-title">{content['testimonials']['title']}</h2>
            <div class="testimonials-grid">'''
        
        for review in content['testimonials']['reviews']:
            stars = '⭐' * review['rating']
            html += f'''
                <div class="testimonial">
                    <div style="font-style: italic; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">"{review['text']}"</div>
                    <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.5rem;">{review['name']}, {review['role']}</div>
                    <div>{stars}</div>
                </div>'''
        
        # Enhanced pricing section
        original_price = content['pricing'].get('original_price', '')
        guarantee = content['pricing'].get('guarantee', '')
        
        html += f'''
            </div>
        </div>
    </section>

    <section id="pricing" class="section pricing">
        <div class="container">
            <h2 class="section-title">{content['pricing']['title']}</h2>
            <div class="pricing-card">
                {f'<div class="original-price">{original_price}</div>' if original_price else ''}
                <div class="price">{content['pricing']['price']}</div>
                <ul class="pricing-features">'''
        
        for feature in content['pricing']['features']:
            html += f'                    <li>{feature}</li>\n'
        
        html += f'''
                </ul>
                <a href="#" class="cta-button">{content['pricing']['cta']}</a>
                {f'<p style="margin-top: 2rem; opacity: 0.9; font-size: 0.9rem;">{guarantee}</p>' if guarantee else ''}
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {product_name}. All rights reserved.</p>
            <p style="margin-top: 1rem; opacity: 0.7;">Powered by Enhanced AI Site Generator</p>
        </div>
    </footer>
</body>
</html>'''
        
        return html

    def _generate_relevant_catalog_products(self, product_name: str, category: str, main_word: str) -> List[Dict]:
        """Generate truly relevant catalog products with specific image prompts"""
        
        # Extract key product characteristics
        product_lower = product_name.lower()
        
        if category == "technology":
            if "laptop" in product_lower or "computer" in product_lower:
                return [
                    {"name": "Gaming Mouse & Keyboard Set", "price": "$89", "image_prompt": f"professional product photo of gaming mouse and mechanical keyboard set on white background"},
                    {"name": "Laptop Cooling Pad", "price": "$59", "image_prompt": f"professional product photo of laptop cooling pad with fans on white background"},
                    {"name": "External Monitor 24 inch", "price": "$199", "image_prompt": f"professional product photo of 24 inch computer monitor on white background"},
                    {"name": "Laptop Travel Case", "price": "$49", "image_prompt": f"professional product photo of protective laptop bag case on white background"}
                ]
            elif "phone" in product_lower or "smartphone" in product_lower:
                return [
                    {"name": "Wireless Charging Pad", "price": "$39", "image_prompt": f"professional product photo of wireless phone charging pad on white background"},
                    {"name": "Phone Screen Protector", "price": "$19", "image_prompt": f"professional product photo of tempered glass screen protector on white background"},
                    {"name": "Bluetooth Headphones", "price": "$129", "image_prompt": f"professional product photo of wireless bluetooth headphones on white background"},
                    {"name": "Phone Camera Lens Kit", "price": "$79", "image_prompt": f"professional product photo of smartphone camera lens attachment kit on white background"}
                ]
            elif "headphone" in product_lower or "earphone" in product_lower:
                return [
                    {"name": "Headphone Stand", "price": "$29", "image_prompt": f"professional product photo of wooden headphone stand on white background"},
                    {"name": "Audio Cable Set", "price": "$25", "image_prompt": f"professional product photo of premium audio cables set on white background"},
                    {"name": "Foam Ear Cushions", "price": "$19", "image_prompt": f"professional product photo of replacement headphone ear cushions on white background"},
                    {"name": "Portable Amplifier", "price": "$159", "image_prompt": f"professional product photo of portable headphone amplifier on white background"}
                ]
            else:
                # Generic tech accessories
                return [
                    {"name": f"{main_word.title()} Carrying Case", "price": "$39", "image_prompt": f"professional product photo of {product_name} protective carrying case on white background"},
                    {"name": f"{main_word.title()} Cable Set", "price": "$29", "image_prompt": f"professional product photo of {product_name} cables and adapters on white background"},
                    {"name": f"{main_word.title()} Mount Stand", "price": "$49", "image_prompt": f"professional product photo of {product_name} adjustable stand mount on white background"},
                    {"name": f"{main_word.title()} Cleaning Kit", "price": "$19", "image_prompt": f"professional product photo of {product_name} cleaning and maintenance kit on white background"}
                ]
                
        elif category == "food_beverage":
            if "coffee" in product_lower:
                return [
                    {"name": "Coffee Grinder", "price": "$79", "image_prompt": f"professional product photo of electric coffee bean grinder on white background"},
                    {"name": "French Press", "price": "$45", "image_prompt": f"professional product photo of glass french press coffee maker on white background"},
                    {"name": "Coffee Storage Canister", "price": "$29", "image_prompt": f"professional product photo of airtight coffee bean storage container on white background"},
                    {"name": "Coffee Filter Papers", "price": "$15", "image_prompt": f"professional product photo of premium coffee filter papers pack on white background"}
                ]
            elif "tea" in product_lower:
                return [
                    {"name": "Tea Infuser Set", "price": "$25", "image_prompt": f"professional product photo of stainless steel tea infuser strainer on white background"},
                    {"name": "Tea Storage Tins", "price": "$35", "image_prompt": f"professional product photo of decorative tea storage tin set on white background"},
                    {"name": "Electric Kettle", "price": "$89", "image_prompt": f"professional product photo of electric tea kettle on white background"},
                    {"name": "Tea Cup Set", "price": "$55", "image_prompt": f"professional product photo of elegant ceramic tea cup set on white background"}
                ]
            elif any(fruit in product_lower for fruit in ["apple", "banana", "orange", "fruit"]):
                return [
                    {"name": "Fruit Storage Basket", "price": "$25", "image_prompt": f"professional product photo of woven fruit storage basket on white background"},
                    {"name": "Fruit Washing Bowl", "price": "$19", "image_prompt": f"professional product photo of large fruit washing colander bowl on white background"},
                    {"name": "Fruit Knife Set", "price": "$39", "image_prompt": f"professional product photo of sharp fruit cutting knives set on white background"},
                    {"name": "Fruit Dehydrator", "price": "$129", "image_prompt": f"professional product photo of electric fruit dehydrator machine on white background"}
                ]
            else:
                # Generic food accessories
                return [
                    {"name": f"{main_word.title()} Storage Container", "price": "$29", "image_prompt": f"professional product photo of {product_name} airtight storage container on white background"},
                    {"name": f"{main_word.title()} Serving Set", "price": "$45", "image_prompt": f"professional product photo of {product_name} serving utensils set on white background"},
                    {"name": f"{main_word.title()} Recipe Book", "price": "$25", "image_prompt": f"professional product photo of {product_name} cookbook recipe book on white background"},
                    {"name": f"Premium {main_word.title()} Sampler", "price": "$35", "image_prompt": f"professional product photo of {product_name} variety sampler pack on white background"}
                ]
                
        elif category == "health_wellness":
            if "yoga" in product_lower or "mat" in product_lower:
                return [
                    {"name": "Yoga Block Set", "price": "$29", "image_prompt": f"professional product photo of foam yoga blocks set on white background"},
                    {"name": "Yoga Strap", "price": "$15", "image_prompt": f"professional product photo of cotton yoga stretching strap on white background"},
                    {"name": "Yoga Towel", "price": "$25", "image_prompt": f"professional product photo of non-slip yoga towel on white background"},
                    {"name": "Yoga Ball", "price": "$35", "image_prompt": f"professional product photo of exercise yoga ball on white background"}
                ]
            elif "supplement" in product_lower or "vitamin" in product_lower:
                return [
                    {"name": "Pill Organizer", "price": "$19", "image_prompt": f"professional product photo of weekly pill organizer case on white background"},
                    {"name": "Shaker Bottle", "price": "$25", "image_prompt": f"professional product photo of protein shaker bottle on white background"},
                    {"name": "Digital Scale", "price": "$39", "image_prompt": f"professional product photo of digital kitchen supplement scale on white background"},
                    {"name": "Supplement Storage", "price": "$29", "image_prompt": f"professional product photo of supplement storage organizer on white background"}
                ]
            elif "fitness" in product_lower or "gym" in product_lower:
                return [
                    {"name": "Resistance Bands Set", "price": "$25", "image_prompt": f"professional product photo of fitness resistance bands set on white background"},
                    {"name": "Water Bottle", "price": "$19", "image_prompt": f"professional product photo of sports water bottle on white background"},
                    {"name": "Workout Towel", "price": "$15", "image_prompt": f"professional product photo of microfiber workout towel on white background"},
                    {"name": "Gym Bag", "price": "$49", "image_prompt": f"professional product photo of fitness gym duffel bag on white background"}
                ]
            else:
                # Generic wellness accessories
                return [
                    {"name": f"{main_word.title()} Tracking Journal", "price": "$25", "image_prompt": f"professional product photo of {product_name} progress tracking journal on white background"},
                    {"name": f"{main_word.title()} Instruction Guide", "price": "$19", "image_prompt": f"professional product photo of {product_name} instruction manual guide on white background"},
                    {"name": f"{main_word.title()} Care Kit", "price": "$35", "image_prompt": f"professional product photo of {product_name} maintenance care kit on white background"},
                    {"name": f"{main_word.title()} Travel Case", "price": "$29", "image_prompt": f"professional product photo of {product_name} portable travel case on white background"}
                ]
                
        elif category == "fashion":
            if "dress" in product_lower or "shirt" in product_lower or "clothing" in product_lower:
                return [
                    {"name": "Garment Steamer", "price": "$59", "image_prompt": f"professional product photo of handheld garment steamer on white background"},
                    {"name": "Clothing Brush", "price": "$25", "image_prompt": f"professional product photo of premium clothing lint brush on white background"},
                    {"name": "Hanger Set", "price": "$35", "image_prompt": f"professional product photo of velvet clothing hangers set on white background"},
                    {"name": "Garment Bag", "price": "$29", "image_prompt": f"professional product photo of breathable garment storage bag on white background"}
                ]
            elif "shoe" in product_lower or "boot" in product_lower:
                return [
                    {"name": "Shoe Care Kit", "price": "$39", "image_prompt": f"professional product photo of leather shoe care cleaning kit on white background"},
                    {"name": "Shoe Insoles", "price": "$19", "image_prompt": f"professional product photo of comfort shoe insoles on white background"},
                    {"name": "Shoe Rack", "price": "$45", "image_prompt": f"professional product photo of wooden shoe storage rack on white background"},
                    {"name": "Shoe Horn", "price": "$15", "image_prompt": f"professional product photo of long handle shoe horn on white background"}
                ]
            else:
                # Generic fashion accessories
                return [
                    {"name": f"{main_word.title()} Care Instructions", "price": "$15", "image_prompt": f"professional product photo of {product_name} care instruction card on white background"},
                    {"name": f"{main_word.title()} Storage Box", "price": "$25", "image_prompt": f"professional product photo of {product_name} storage box organizer on white background"},
                    {"name": f"{main_word.title()} Accessories", "price": "$35", "image_prompt": f"professional product photo of {product_name} matching accessories on white background"},
                    {"name": f"{main_word.title()} Gift Box", "price": "$19", "image_prompt": f"professional product photo of {product_name} luxury gift box on white background"}
                ]
        else:
            # Default generic accessories
            return [
                {"name": f"{main_word.title()} User Manual", "price": "$19", "image_prompt": f"professional product photo of {product_name} instruction manual on white background"},
                {"name": f"{main_word.title()} Starter Kit", "price": "$39", "image_prompt": f"professional product photo of {product_name} beginner starter kit on white background"},
                {"name": f"{main_word.title()} Maintenance Set", "price": "$29", "image_prompt": f"professional product photo of {product_name} maintenance tools set on white background"},
                {"name": f"{main_word.title()} Upgrade Pack", "price": "$59", "image_prompt": f"professional product photo of {product_name} premium upgrade pack on white background"}
            ]

    def _enhanced_fallback_content(self, product_name: str, category: str) -> Dict[str, Any]:
        """Ultra-dynamic fallback content with sophisticated content generation"""
        print(f"🎨 Creating ultra-dynamic content for {product_name} ({category})")
        
        # Import for content generation
        import random
        from datetime import datetime
        
        # Extract key words from product name for content customization
        product_words = product_name.lower().split()
        main_word = product_words[0] if product_words else "product"
        
        # Ultra-sophisticated category-specific content templates
        category_templates = {
            "technology": {
                "adjectives": ["Revolutionary", "Next-Generation", "AI-Powered", "Smart", "Advanced", "Cutting-Edge", "Innovative", "High-Performance"],
                                 "benefits": [
                     {"icon": "🚀", "title": "Lightning Performance", "description": f"Experience blazing-fast {main_word} speeds with our optimized architecture"},
                     {"icon": "🤖", "title": "Smart Intelligence", "description": f"Advanced AI learns your {main_word} usage patterns for maximum efficiency"},
                     {"icon": "🔒", "title": "Enterprise Security", "description": f"Military-grade encryption keeps your {main_word} data completely secure"},
                     {"icon": "⚡", "title": "Instant Connectivity", "description": f"Seamless {main_word} integration across all your devices and platforms"},
                     {"icon": "📊", "title": "Smart Analytics", "description": f"Real-time insights and predictive {main_word} performance monitoring"},
                     {"icon": "🎯", "title": "Precision Control", "description": f"Fine-tune every aspect of your {main_word} for perfect optimization"}
                 ],
                                 "steps": [
                     {"title": "Quick Setup", "description": f"Download and install your {product_name} in under 5 minutes"},
                     {"title": "Smart Configuration", "description": f"Our AI automatically optimizes {product_name} for your specific needs"},
                     {"title": "Experience Results", "description": f"Start seeing improved {main_word} performance immediately"}
                 ],
                "testimonials": [
                    {"name": "Alex Chen", "role": "Senior Developer", "text": f"This {product_name} completely transformed my workflow. The performance gains are incredible!"},
                    {"name": "Sarah Martinez", "role": "Tech Lead", "text": f"I've tried many {main_word} solutions, but {product_name} is in a league of its own."}
                ],
                "related_products": [
                    {"name": f"Pro {main_word.title()} Extension", "price": random.choice(["$29", "$39", "$49"])},
                    {"name": f"{main_word.title()} Analytics Dashboard", "price": random.choice(["$59", "$79", "$99"])},
                    {"name": f"Enterprise {main_word.title()} Suite", "price": random.choice(["$149", "$199", "$249"])},
                    {"name": f"{main_word.title()} Security Pack", "price": random.choice(["$39", "$59", "$79"])}
                ]
            },
                         "food_beverage": {
                 "adjectives": ["Artisan", "Premium", "Organic", "Farm-Fresh", "Gourmet", "Handcrafted", "Traditional", "Authentic"],
                 "benefits": [
                     {"icon": "🌿", "title": "100% Organic", "description": f"Our {product_name} is grown without pesticides or artificial additives"},
                     {"icon": "👨‍🍳", "title": "Chef Approved", "description": f"Endorsed by Michelin-starred chefs for exceptional {main_word} quality"},
                     {"icon": "🏆", "title": "Award Winning", "description": f"Multiple international awards for outstanding {main_word} excellence"},
                     {"icon": "🌍", "title": "Sustainable Sourcing", "description": f"Ethically sourced {main_word} supporting local farming communities"},
                     {"icon": "📦", "title": "Fresh Delivery", "description": f"Your {product_name} arrives fresh within 24-48 hours of harvest"},
                     {"icon": "✨", "title": "Artisan Quality", "description": f"Hand-selected {main_word} with traditional preparation methods"}
                 ],
                                 "steps": [
                     {"title": "Select & Order", "description": f"Choose your preferred {product_name} variety and quantity"},
                     {"title": "Fresh Preparation", "description": f"We carefully prepare and package your {main_word} order"},
                     {"title": "Enjoy Premium Quality", "description": f"Savor the exceptional taste and quality of our {product_name}"}
                 ],
                "testimonials": [
                    {"name": "Maria Rodriguez", "role": "Food Blogger", "text": f"The {product_name} exceeded all my expectations. Absolutely divine taste!"},
                    {"name": "Chef Robert Wilson", "role": "Executive Chef", "text": f"I use this {product_name} in my restaurant. My customers always ask about the secret ingredient."}
                ],
                "related_products": [
                    {"name": f"Premium {main_word.title()} Sampler", "price": random.choice(["$25", "$35", "$45"])},
                    {"name": f"{main_word.title()} Storage Container", "price": random.choice(["$19", "$29", "$39"])},
                    {"name": f"Artisan {main_word.title()} Collection", "price": random.choice(["$75", "$99", "$125"])},
                    {"name": f"{main_word.title()} Recipe Book", "price": random.choice(["$15", "$25", "$35"])},
                ]
            },
                         "health_wellness": {
                 "adjectives": ["Clinical-Grade", "Doctor-Recommended", "Scientifically-Proven", "Premium", "Professional", "Advanced", "Therapeutic", "Medical-Grade"],
                 "benefits": [
                     {"icon": "🔬", "title": "Clinically Tested", "description": f"Our {product_name} is validated through rigorous clinical studies"},
                     {"icon": "👨‍⚕️", "title": "Doctor Endorsed", "description": f"Recommended by healthcare professionals for {main_word} therapy"},
                     {"icon": "📈", "title": "Proven Results", "description": f"95% of users report significant {main_word} improvement within 30 days"},
                     {"icon": "🧬", "title": "Advanced Formula", "description": f"Cutting-edge biotechnology enhances {main_word} effectiveness"},
                     {"icon": "🛡️", "title": "Safe & Natural", "description": f"FDA-approved {product_name} with zero harmful side effects"},
                     {"icon": "⚡", "title": "Fast Acting", "description": f"Notice {main_word} improvements within the first week of use"}
                 ],
                                 "steps": [
                     {"title": "Consultation", "description": f"Take our assessment to determine the best {product_name} approach"},
                     {"title": "Personalized Plan", "description": f"Receive your customized {main_word} improvement program"},
                     {"title": "Track Progress", "description": f"Monitor your {main_word} improvements with our tracking tools"}
                 ],
                "testimonials": [
                    {"name": "Dr. Jennifer Lee", "role": "Wellness Specialist", "text": f"I recommend {product_name} to all my patients seeking {main_word} improvement."},
                    {"name": "Michael Thompson", "role": "Fitness Coach", "text": f"The {product_name} transformed my clients' {main_word} performance dramatically."}
                ],
                "related_products": [
                    {"name": f"{main_word.title()} Monitoring Kit", "price": random.choice(["$79", "$99", "$129"])},
                    {"name": f"Advanced {main_word.title()} Support", "price": random.choice(["$39", "$59", "$79"])},
                    {"name": f"{main_word.title()} Recovery Bundle", "price": random.choice(["$149", "$199", "$249"])},
                    {"name": f"Professional {main_word.title()} Guide", "price": random.choice(["$29", "$39", "$49"])},
                ]
            },
                         "fashion": {
                 "adjectives": ["Designer", "Luxury", "Exclusive", "Handcrafted", "Premium", "Couture", "Elegant", "Sophisticated"],
                 "benefits": [
                     {"icon": "✨", "title": "Luxury Design", "description": f"Exquisite {product_name} crafted by renowned fashion designers"},
                     {"icon": "🏆", "title": "Premium Materials", "description": f"Finest quality materials used in every {main_word} piece"},
                     {"icon": "👗", "title": "Perfect Fit", "description": f"Tailored {main_word} sizing for the most flattering silhouette"},
                     {"icon": "🌟", "title": "Trend Setting", "description": f"Stay ahead of fashion with our exclusive {product_name} collection"},
                     {"icon": "💎", "title": "Attention to Detail", "description": f"Meticulous craftsmanship in every {main_word} element"},
                     {"icon": "🎨", "title": "Versatile Style", "description": f"Our {product_name} transitions seamlessly from day to night"}
                 ],
                                 "steps": [
                     {"title": "Browse Collection", "description": f"Explore our curated {product_name} styles and designs"},
                     {"title": "Perfect Sizing", "description": f"Use our size guide to find your ideal {main_word} fit"},
                     {"title": "Style Confidently", "description": f"Rock your new {product_name} with complete confidence"}
                 ],
                "testimonials": [
                    {"name": "Isabella Fashion", "role": "Style Influencer", "text": f"This {product_name} is absolutely stunning! I get compliments everywhere I go."},
                    {"name": "Amanda Style", "role": "Fashion Blogger", "text": f"The quality and design of this {product_name} is unmatched. Pure perfection!"}
                ],
                "related_products": [
                    {"name": f"{main_word.title()} Care Kit", "price": random.choice(["$25", "$35", "$45"])},
                    {"name": f"Matching {main_word.title()} Accessories", "price": random.choice(["$59", "$79", "$99"])},
                    {"name": f"Designer {main_word.title()} Collection", "price": random.choice(["$149", "$199", "$299"])},
                    {"name": f"Limited Edition {main_word.title()}", "price": random.choice(["$199", "$299", "$399"])},
                ]
            }
        }
        
        # Default to technology if category not found
        template_data = category_templates.get(category, category_templates["technology"])
        
        # Generate dynamic content
        adjective = random.choice(template_data["adjectives"])
        benefits = random.sample(template_data["benefits"], 6)  # Random selection of 6 benefits
        steps = template_data["steps"]
        testimonials = random.sample(template_data["testimonials"], 2)
        related_products = template_data["related_products"]
        
        # Generate realistic pricing
        base_price = random.randint(99, 899)
        original_price = base_price + random.randint(50, 200)
        
        # Generate dynamic headlines and descriptions
        headlines = [
            f"{adjective} {product_name}",
            f"The Ultimate {product_name} Experience",
            f"Professional-Grade {product_name}",
            f"Premium {product_name} Solution"
        ]
        
        taglines = [
            f"Discover what makes {product_name} extraordinary",
            f"Experience the difference quality makes",
            f"Engineered for excellence, designed for you",
            f"Where innovation meets perfection"
        ]
        
        descriptions = [
            f"Experience the revolutionary {product_name} that's changing everything. Engineered with precision and designed for maximum performance.",
            f"Discover why thousands choose our {product_name}. Premium quality, exceptional results, unmatched satisfaction.",
            f"Transform your experience with our premium {product_name}. Advanced features, superior quality, guaranteed results."
        ]
        
        cta_buttons = [
            f"Get {product_name} Now",
            f"Order Your {product_name}",
            f"Start with {product_name}",
            f"Buy {product_name} Today"
        ]
        
        # Create the comprehensive content structure
        content = {
            "hero": {
                "headline": random.choice(headlines),
                "subheadline": random.choice(taglines),
                "description": random.choice(descriptions),
                "cta_button": random.choice(cta_buttons)
            },
            "features": {
                "title": f"Why {product_name} is Different",
                "items": benefits
            },
            "how_it_works": {
                "title": f"Getting Started with {product_name}",
                                 "steps": [{"step": i+1, "title": step["title"], "description": step["description"]} for i, step in enumerate(steps)]
            },
            "testimonials": {
                "title": "What Our Customers Say",
                "reviews": [{"name": t["name"], "role": t["role"], "text": t["text"], "rating": 5} for t in testimonials]
            },
            "catalog": {
                "title": "Complete Your Setup",
                "description": f"Perfect accessories and add-ons for your {product_name}",
                "products": self._generate_relevant_catalog_products(product_name, category, main_word)
            },
            "pricing": {
                "title": f"Get Your {product_name} Today",
                "price": f"${base_price}",
                "original_price": f"${original_price}",
                "features": [
                    f"Complete {product_name} package",
                    "Free shipping & handling",
                    "24/7 customer support",
                    "Setup assistance included",
                    "Premium warranty coverage"
                ],
                "cta": "Buy {product_name}",
                "guarantee": random.choice(["30-day performance guarantee", "60-day satisfaction guarantee", "90-day money-back guarantee"])
            },
            "tagline": f"Experience the {adjective.lower()} difference",
            "meta_description": f"Get the best {product_name} - {adjective.lower()} solution with premium features, expert support, and guaranteed satisfaction."
        }
        
        print(f"✅ Generated ultra-dynamic content with {len(benefits)} unique features")
        return content

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gpt_site_generator.py 'Product Name'")
        sys.exit(1)
    
    product_name = sys.argv[1]
    generator = EnhancedGPTSiteGenerator()
    
    try:
        result = generator.generate_website(product_name)
        print(f"SUCCESS:{result}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 