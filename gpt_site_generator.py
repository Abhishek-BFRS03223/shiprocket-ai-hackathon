#!/usr/bin/env python3
"""
GPT-Powered Dynamic Site Generator
Uses GPT API to generate unique website content for any product
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# Pexels API integration
PEXELS_API_KEY = "gK2KUUNX6SpIkoxzSf1oRRLQEtBlOEV2vRx3PWb1SP6XvkfH9QDvOKOy"

def get_pexels_image(search_term, size="large"):
    """Get high-quality image from Pexels API"""
    try:
        headers = {
            'Authorization': PEXELS_API_KEY
        }
        url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=1&size={size}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                return data['photos'][0]['src']['large']
    except Exception as e:
        print(f"Pexels API error: {e}")
    
    # Fallback to Unsplash
    return f"https://source.unsplash.com/1920x1080/?{search_term.replace(' ', '+')}"

class GPTSiteGenerator:
    def __init__(self):
        """Initialize GPT Site Generator with OpenAI API"""
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        if not self.api_key:
            print("⚠️ No OpenAI API key found. Running in fallback mode.")
            print("Get your API key from: https://platform.openai.com/api-keys")
        
        self.output_dir = "generated_sites"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def categorize_product(self, product_name: str) -> str:
        """Use GPT to intelligently categorize product"""
        if not self.api_key:
            # Simple fallback categorization
            product_lower = product_name.lower()
            if any(word in product_lower for word in ['tech', 'smart', 'ai', 'digital', 'app', 'software', 'device', 'phone', 'laptop', 'drone']):
                return "technology"
            elif any(word in product_lower for word in ['food', 'coffee', 'restaurant', 'kitchen', 'recipe', 'meal', 'drink']):
                return "food_beverage"
            elif any(word in product_lower for word in ['fashion', 'clothing', 'dress', 'shoes', 'bag', 'jewelry', 'style']):
                return "fashion"
            elif any(word in product_lower for word in ['health', 'fitness', 'wellness', 'yoga', 'gym', 'medical', 'care']):
                return "health_wellness"
            elif any(word in product_lower for word in ['business', 'consulting', 'service', 'management', 'corporate']):
                return "business"
            else:
                return "general"
        
        try:
            prompt = f"""
            Categorize this product into one of these categories: technology, food_beverage, fashion, health_wellness, business
            
            Product: {product_name}
            
            Return only the category name (one word).
            """
            
            response = self._call_openai_api(prompt, max_tokens=10)
            if response:
                category = response.strip().lower()
                valid_categories = ["technology", "food_beverage", "fashion", "health_wellness", "business"]
                return category if category in valid_categories else "general"
            else:
                return "general"
                
        except Exception as e:
            print(f"GPT categorization failed: {e}")
            return "general"
    
    def _call_openai_api(self, prompt: str, max_tokens: int = 1500) -> str:
        """Call OpenAI API using requests"""
        if not self.api_key:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"OpenAI API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return None
    
    def generate_website_content(self, product_name: str, category: str) -> Dict[str, Any]:
        """Use GPT to generate unique website content"""
        if not self.api_key:
            return self._fallback_content(product_name, category)
        
        try:
            prompt = f"""
            Generate comprehensive website content for a product called "{product_name}" in the {category} category.
            
            Create content for these sections:
            1. Hero section (headline, subheadline, description)
            2. Key features (6 unique features)
            3. Benefits (4 compelling benefits)
            4. How it works (3 steps)
            5. Testimonials (2 realistic customer reviews)
            6. Pricing section
            7. Call-to-action copy
            
            Requirements:
            - Make it unique and specific to {product_name}
            - Use persuasive, professional copywriting
            - Include specific details that make sense for this product
            - Avoid generic language
            - Focus on benefits, not just features
            
            Return as JSON with this structure:
            {{
                "hero": {{
                    "headline": "Main headline",
                    "subheadline": "Supporting headline", 
                    "description": "Detailed description",
                    "cta_button": "Button text"
                }},
                "features": {{
                    "title": "Section title",
                    "list": ["feature1", "feature2", "feature3", "feature4", "feature5", "feature6"]
                }},
                "benefits": {{
                    "title": "Section title",
                    "list": ["benefit1", "benefit2", "benefit3", "benefit4"]
                }},
                "how_it_works": {{
                    "title": "Section title",
                    "steps": [
                        {{"step": 1, "title": "Step title", "description": "Step description"}},
                        {{"step": 2, "title": "Step title", "description": "Step description"}},
                        {{"step": 3, "title": "Step title", "description": "Step description"}}
                    ]
                }},
                "testimonials": {{
                    "title": "Section title",
                    "reviews": [
                        {{"name": "Customer name", "role": "Their role/job", "text": "Testimonial text", "rating": 5}},
                        {{"name": "Customer name", "role": "Their role/job", "text": "Testimonial text", "rating": 5}}
                    ]
                }},
                "pricing": {{
                    "title": "Section title",
                    "price": "$XX",
                    "features": ["included feature 1", "included feature 2", "included feature 3"],
                    "cta": "Purchase button text"
                }},
                "tagline": "Memorable product tagline",
                "meta_description": "SEO meta description"
            }}
            """
            
            response = self._call_openai_api(prompt, max_tokens=2000)
            
            if response:
                content_text = response.strip()
                
                # Try to parse JSON
                try:
                    content = json.loads(content_text)
                    return content
                except json.JSONDecodeError:
                    # Extract JSON from response if wrapped in markdown
                    if "```json" in content_text:
                        json_start = content_text.find("```json") + 7
                        json_end = content_text.find("```", json_start)
                        content_text = content_text[json_start:json_end].strip()
                        content = json.loads(content_text)
                        return content
                    else:
                        print("Failed to parse GPT response as JSON")
                        return self._fallback_content(product_name, category)
            else:
                return self._fallback_content(product_name, category)
                    
        except Exception as e:
            print(f"GPT content generation failed: {e}")
            return self._fallback_content(product_name, category)
    
    def generate_website(self, product_name: str) -> str:
        """Generate complete website using GPT"""
        print(f"🔍 Analyzing product: {product_name}")
        
        # Step 1: Categorize product using GPT
        category = self.categorize_product(product_name)
        print(f"📂 Category detected: {category}")
        
        # Step 2: Generate content using GPT
        if self.api_key:
            print(f"📝 Generating dynamic content with GPT...")
        else:
            print(f"📝 Generating enhanced content (fallback mode)...")
        content = self.generate_website_content(product_name, category)
        
        # Step 3: Generate HTML
        print(f"🌐 Building responsive website...")
        html = self.generate_html(product_name, content, category)
        
        # Step 4: Save website
        site_dir = os.path.join(self.output_dir, product_name.lower().replace(' ', '_'))
        os.makedirs(site_dir, exist_ok=True)
        
        # Save HTML
        html_file = os.path.join(site_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Save metadata
        metadata = {
            'name': product_name,
            'category': category,
            'generated_at': datetime.now().isoformat(),
            'tagline': content['tagline'],
            'description': content['meta_description'],
            'features': content['features']['list'],
            'generation_method': 'GPT-Powered Dynamic Content',
            'api_used': 'OpenAI GPT-3.5-turbo' if self.api_key else 'Enhanced Fallback Mode'
        }
        
        metadata_file = os.path.join(site_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ GPT-powered website generated successfully!")
        return site_dir

    def generate_html(self, product_name: str, content: Dict, category: str) -> str:
        """Generate responsive HTML website"""
        
        # Category-based color schemes
        color_schemes = {
            "technology": {"primary": "#007ACC", "secondary": "#F8F9FA", "accent": "#FF6B6B", "text": "#2C3E50"},
            "food_beverage": {"primary": "#FF6B35", "secondary": "#FFF8E1", "accent": "#4CAF50", "text": "#2C3E50"},
            "fashion": {"primary": "#E91E63", "secondary": "#FCE4EC", "accent": "#9C27B0", "text": "#2C3E50"},
            "health_wellness": {"primary": "#4CAF50", "secondary": "#E8F5E8", "accent": "#2196F3", "text": "#2C3E50"},
            "business": {"primary": "#2C3E50", "secondary": "#ECF0F1", "accent": "#3498DB", "text": "#2C3E50"},
            "general": {"primary": "#3498DB", "secondary": "#F8F9FA", "accent": "#E74C3C", "text": "#2C3E50"}
        }
        colors = color_schemes.get(category, color_schemes["general"])
        
        # Get real images from free APIs
        hero_bg = get_pexels_image(product_name)
        gallery_images = [
            f"https://picsum.photos/seed/{product_name.replace(' ', '')}-{i}/400/300"
            for i in range(1, 5)
        ]
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name} - {content['tagline']}</title>
    <meta name="description" content="{content['meta_description']}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: {colors['text']}; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        
        .header {{ 
            background: {colors['primary']}; color: white; padding: 1rem 0; 
            position: fixed; width: 100%; top: 0; z-index: 1000; 
        }}
        .nav {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 1.5rem; font-weight: bold; color: white; text-decoration: none; }}
        .nav-links {{ display: flex; list-style: none; gap: 2rem; }}
        .nav-links a {{ color: white; text-decoration: none; }}
        
        .hero {{
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{hero_bg}');
            background-size: cover; background-position: center; height: 100vh;
            display: flex; align-items: center; color: white; text-align: center;
        }}
        .hero h1 {{ font-size: 3.5rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.3rem; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto; }}
        
        .cta-button {{
            background: {colors['accent']}; color: white; padding: 15px 30px;
            text-decoration: none; border-radius: 50px; font-weight: bold;
            display: inline-block; transition: transform 0.3s;
        }}
        .cta-button:hover {{ transform: translateY(-2px); }}
        
        .section {{ padding: 80px 0; }}
        .section-title {{ text-align: center; font-size: 2.5rem; margin-bottom: 3rem; color: {colors['primary']}; }}
        
        .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
        .feature-card {{ background: white; padding: 2rem; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .feature-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
        
        .steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }}
        .step {{ text-align: center; padding: 2rem; }}
        .step-number {{
            background: {colors['primary']}; color: white; width: 60px; height: 60px;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold; margin: 0 auto 1rem;
        }}
        
        .testimonials {{ background: white; }}
        .testimonials-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
        .testimonial {{ background: {colors['secondary']}; padding: 2rem; border-radius: 10px; border-left: 4px solid {colors['accent']}; }}
        
        .gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }}
        .gallery img {{ width: 100%; height: 200px; object-fit: cover; border-radius: 10px; }}
        
        .pricing {{ background: {colors['primary']}; color: white; text-align: center; }}
        .price {{ font-size: 3rem; font-weight: bold; margin: 1rem 0; }}
        .pricing-features {{ list-style: none; margin: 2rem 0; }}
        .pricing-features li {{ padding: 0.5rem 0; }}
        
        .footer {{ background: {colors['text']}; color: white; text-align: center; padding: 3rem 0; }}
        
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2.5rem; }}
            .nav-links {{ display: none; }}
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
            <div class="features-grid">
"""
        
        # Add feature cards
        icons = ['🚀', '⭐', '💎', '🔥', '⚡', '🎯']
        for i, feature in enumerate(content['features']['list']):
            icon = icons[i % len(icons)]
            html += f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3>{feature}</h3>
                </div>"""
        
        html += f"""
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <h2 class="section-title">{content['how_it_works']['title']}</h2>
            <div class="steps">
"""
        
        for step in content['how_it_works']['steps']:
            html += f"""
                <div class="step">
                    <div class="step-number">{step['step']}</div>
                    <h3>{step['title']}</h3>
                    <p>{step['description']}</p>
                </div>"""
        
        html += f"""
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <h2 class="section-title">Gallery</h2>
            <div class="gallery">
"""
        
        for img in gallery_images:
            html += f'                <img src="{img}" alt="{product_name}" loading="lazy">\n'
        
        html += f"""
            </div>
        </div>
    </section>

    <section id="testimonials" class="section testimonials">
        <div class="container">
            <h2 class="section-title">{content['testimonials']['title']}</h2>
            <div class="testimonials-grid">
"""
        
        for review in content['testimonials']['reviews']:
            stars = '⭐' * review['rating']
            html += f"""
                <div class="testimonial">
                    <div style="font-style: italic; margin-bottom: 1rem;">"{review['text']}"</div>
                    <div style="font-weight: bold; color: {colors['primary']};">{review['name']}, {review['role']}</div>
                    <div style="margin-top: 0.5rem;">{stars}</div>
                </div>"""
        
        html += f"""
            </div>
        </div>
    </section>

    <section id="pricing" class="section pricing">
        <div class="container">
            <h2 class="section-title">{content['pricing']['title']}</h2>
            <div class="price">{content['pricing']['price']}</div>
            <ul class="pricing-features">
"""
        
        for feature in content['pricing']['features']:
            html += f'                <li>✓ {feature}</li>\n'
        
        html += f"""
            </ul>
            <a href="#" class="cta-button">{content['pricing']['cta']}</a>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {product_name}. All rights reserved.</p>
            <p>Generated by GPT-Powered Site Generator</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html

    def _fallback_content(self, product_name: str, category: str) -> Dict[str, Any]:
        """Enhanced fallback content that's product-specific"""
        
        # Category-specific content templates
        category_content = {
            "technology": {
                "headline_prefix": "Revolutionary",
                "features": ["AI-Powered Technology", "Advanced Analytics", "Seamless Integration", "Real-Time Processing", "Smart Automation", "Cutting-Edge Security"],
                "benefits": ["Boost Productivity by 300%", "Reduce Costs Significantly", "Streamline Operations", "Future-Proof Solution"],
                "price": "$299"
            },
            "food_beverage": {
                "headline_prefix": "Artisanal",
                "features": ["Premium Quality Ingredients", "Authentic Flavors", "Handcrafted Excellence", "Sustainable Sourcing", "Fresh Daily", "Expert Curation"],
                "benefits": ["Exceptional Taste Experience", "Health-Conscious Choice", "Supporting Local Communities", "Guilt-Free Indulgence"],
                "price": "$89"
            },
            "fashion": {
                "headline_prefix": "Luxury",
                "features": ["Premium Materials", "Timeless Design", "Perfect Fit", "Handcrafted Details", "Exclusive Patterns", "Versatile Style"],
                "benefits": ["Express Your Unique Style", "Confidence Boosting", "Long-Lasting Quality", "Compliments Guaranteed"],
                "price": "$199"
            },
            "health_wellness": {
                "headline_prefix": "Transformative",
                "features": ["Science-Backed Results", "Natural Ingredients", "Personalized Approach", "Expert Guidance", "Proven Effectiveness", "Holistic Benefits"],
                "benefits": ["Improve Your Health", "Boost Energy Levels", "Feel More Confident", "Live Your Best Life"],
                "price": "$149"
            },
            "business": {
                "headline_prefix": "Professional",
                "features": ["Expert Consultation", "Proven Strategies", "Custom Solutions", "24/7 Support", "Industry Expertise", "Measurable Results"],
                "benefits": ["Accelerate Growth", "Reduce Risk", "Save Time", "Maximize ROI"],
                "price": "$499"
            },
            "general": {
                "headline_prefix": "Premium",
                "features": ["High Quality", "Easy to Use", "Reliable Performance", "Great Value", "Expert Support", "Proven Results"],
                "benefits": ["Save Time", "Increase Efficiency", "Professional Results", "Peace of Mind"],
                "price": "$99"
            }
        }
        
        cat_data = category_content.get(category, category_content["general"])
        
        return {
            "hero": {
                "headline": f"{cat_data['headline_prefix']} {product_name}",
                "subheadline": "Innovation Meets Excellence",
                "description": f"Experience the future with {product_name}. Designed for those who demand the best in {category.replace('_', ' ')} solutions.",
                "cta_button": f"Get {product_name} Today"
            },
            "features": {
                "title": f"Why Choose {product_name}?",
                "list": cat_data['features']
            },
            "benefits": {
                "title": "Benefits You'll Love",
                "list": cat_data['benefits']
            },
            "how_it_works": {
                "title": "How It Works",
                "steps": [
                    {"step": 1, "title": "Get Started", "description": f"Order your {product_name} in just a few clicks"},
                    {"step": 2, "title": "Setup", "description": "Quick and easy setup process guided by experts"},
                    {"step": 3, "title": "Enjoy", "description": "Start experiencing the benefits immediately"}
                ]
            },
            "testimonials": {
                "title": "What Our Customers Say",
                "reviews": [
                    {"name": "Sarah Johnson", "role": "Professional User", "text": f"{product_name} exceeded all my expectations! The quality is outstanding.", "rating": 5},
                    {"name": "Mike Chen", "role": "Business Owner", "text": f"Game-changer! {product_name} has transformed how we work. Highly recommended!", "rating": 5}
                ]
            },
            "pricing": {
                "title": "Simple Pricing",
                "price": cat_data['price'],
                "features": ["All features included", "24/7 expert support", "30-day money-back guarantee"],
                "cta": f"Get {product_name} Now"
            },
            "tagline": f"The Future of {category.replace('_', ' ').title()}",
            "meta_description": f"Discover {product_name} - the innovative {category.replace('_', ' ')} solution that's transforming how people work and live."
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gpt_site_generator.py 'Product Name'")
        sys.exit(1)
    
    product_name = sys.argv[1]
    generator = GPTSiteGenerator()
    
    try:
        result = generator.generate_website(product_name)
        print(f"SUCCESS:{result}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 