"""
Simple One-Click Site Generator
No complex dependencies - just pure Python functionality
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any

class SimpleSiteGenerator:
    """Simple website generator with no external AI dependencies"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load predefined templates for different product categories"""
        return {
            "technology": {
                "colors": {"primary": "#007ACC", "secondary": "#F8F9FA", "accent": "#FF6B6B"},
                "tone": "Professional and innovative",
                "sections": ["Hero", "Features", "Benefits", "How It Works", "Pricing", "Contact"]
            },
            "food_beverage": {
                "colors": {"primary": "#FF8C42", "secondary": "#FFF8DC", "accent": "#228B22"},
                "tone": "Warm and inviting",
                "sections": ["Hero", "Menu/Products", "About", "Location", "Reviews", "Contact"]
            },
            "fashion": {
                "colors": {"primary": "#E91E63", "secondary": "#F5F5F5", "accent": "#9C27B0"},
                "tone": "Trendy and aspirational",
                "sections": ["Hero", "Collection", "Style Guide", "Testimonials", "Shop", "Contact"]
            },
            "health_wellness": {
                "colors": {"primary": "#4CAF50", "secondary": "#E8F5E8", "accent": "#2196F3"},
                "tone": "Caring and trustworthy",
                "sections": ["Hero", "Benefits", "How It Works", "Testimonials", "Pricing", "Contact"]
            },
            "general": {
                "colors": {"primary": "#2196F3", "secondary": "#F5F5F5", "accent": "#FF9800"},
                "tone": "Friendly and approachable",
                "sections": ["Hero", "Features", "Benefits", "Testimonials", "Pricing", "Contact"]
            }
        }
    
    def analyze_product(self, product_name: str) -> Dict[str, Any]:
        """Analyze product name and categorize it"""
        name_lower = product_name.lower()
        
        # Simple keyword-based categorization
        if any(word in name_lower for word in ['app', 'software', 'tech', 'smart', 'ai', 'digital', 'code', 'system']):
            category = "technology"
        elif any(word in name_lower for word in ['food', 'restaurant', 'cafe', 'kitchen', 'recipe', 'cook', 'eat']):
            category = "food_beverage"
        elif any(word in name_lower for word in ['fashion', 'clothing', 'style', 'wear', 'dress', 'shirt', 'shoe']):
            category = "fashion"
        elif any(word in name_lower for word in ['health', 'fitness', 'wellness', 'medical', 'care', 'fit', 'gym']):
            category = "health_wellness"
        else:
            category = "general"
        
        template = self.templates[category]
        
        # Extract features from product name
        features = []
        if "smart" in name_lower:
            features.append("AI-powered intelligence")
        if "eco" in name_lower or "green" in name_lower:
            features.append("Environmentally friendly")
        if "pro" in name_lower:
            features.append("Professional grade")
        if "mini" in name_lower or "compact" in name_lower:
            features.append("Compact design")
        if "premium" in name_lower or "luxury" in name_lower:
            features.append("Premium quality")
        
        if not features:
            features = ["High quality", "User-friendly", "Reliable"]
        
        return {
            "product_name": product_name,
            "category": category,
            "template": template,
            "features": features[:3],  # Limit to 3 features
            "target_audience": self._get_target_audience(category),
            "pricing": self._get_sample_pricing(category)
        }
    
    def _get_target_audience(self, category: str) -> str:
        audiences = {
            "technology": "Tech-savvy professionals and early adopters",
            "food_beverage": "Food enthusiasts and families",
            "fashion": "Style-conscious individuals",
            "health_wellness": "Health and wellness focused individuals",
            "general": "General consumers"
        }
        return audiences.get(category, "General consumers")
    
    def _get_sample_pricing(self, category: str) -> str:
        prices = {
            "technology": "$99",
            "food_beverage": "$25",
            "fashion": "$79",
            "health_wellness": "$149",
            "general": "$59"
        }
        return prices.get(category, "$59")
    
    def generate_content(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate website content based on analysis"""
        product_name = analysis["product_name"]
        category = analysis["category"]
        features = analysis["features"]
        
        content = {
            "hero": {
                "headline": f"Discover {product_name}",
                "subheadline": f"Revolutionary innovation that transforms your {self._get_category_focus(category)}",
                "cta_button": "Get Started Today",
                "hero_text": f"Experience the future with {product_name}. Designed for those who demand excellence."
            },
            "features": {
                "section_title": f"Why Choose {product_name}",
                "features_list": [
                    {
                        "title": feature,
                        "description": f"Experience {feature.lower()} like never before with our innovative approach."
                    } for feature in features
                ]
            },
            "benefits": {
                "section_title": "Benefits You'll Love",
                "benefits_list": self._get_category_benefits(category)
            },
            "testimonials": {
                "section_title": "What Our Customers Say",
                "testimonials": [
                    {
                        "name": "Sarah Johnson",
                        "role": "Professional User",
                        "text": f"{product_name} exceeded all my expectations. Highly recommended!"
                    },
                    {
                        "name": "Mike Chen",
                        "role": "Business Owner", 
                        "text": f"Game-changer! {product_name} revolutionized our workflow."
                    }
                ]
            },
            "pricing": {
                "section_title": "Simple Pricing",
                "price": analysis["pricing"],
                "features": ["All features included", "24/7 support", "30-day guarantee"]
            },
            "contact": {
                "section_title": "Ready to Start?",
                "cta_text": f"Join thousands who love {product_name}",
                "cta_button": f"Get {product_name} Now",
                "contact_info": f"Contact us: hello@{product_name.lower().replace(' ', '')}.com"
            }
        }
        
        return content
    
    def _get_category_focus(self, category: str) -> str:
        focuses = {
            "technology": "digital experience",
            "food_beverage": "culinary journey",
            "fashion": "style statement",
            "health_wellness": "wellness routine",
            "general": "daily life"
        }
        return focuses.get(category, "experience")
    
    def _get_category_benefits(self, category: str) -> list:
        benefits = {
            "technology": [
                "Boost productivity and efficiency",
                "Seamless integration with existing tools",
                "Advanced security and reliability"
            ],
            "food_beverage": [
                "Fresh, high-quality ingredients",
                "Authentic flavors and recipes",
                "Convenient and fast service"
            ],
            "fashion": [
                "Premium quality materials",
                "Trendy and timeless designs",
                "Perfect fit and comfort"
            ],
            "health_wellness": [
                "Improve your overall health",
                "Evidence-based approach",
                "Personalized experience"
            ],
            "general": [
                "Save time and increase efficiency",
                "Professional results guaranteed",
                "Easy to use for everyone"
            ]
        }
        return benefits.get(category, benefits["general"])
    
    def generate_html(self, analysis: Dict[str, Any], content: Dict[str, Any]) -> str:
        """Generate complete HTML website"""
        colors = analysis["template"]["colors"]
        product_name = analysis["product_name"]
        
        # Extract content sections
        hero = content["hero"]
        features = content["features"]
        benefits = content["benefits"]
        testimonials = content["testimonials"]
        pricing = content["pricing"]
        contact = content["contact"]
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hero['headline']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, {colors['primary']} 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .hero p {{
            font-size: 1.3rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .cta-button {{
            background: {colors['accent']};
            color: white;
            padding: 15px 35px;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        /* Sections */
        .section {{
            padding: 80px 0;
        }}
        
        .section:nth-child(even) {{
            background: {colors['secondary']};
        }}
        
        .section-title {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 50px;
            color: #2c3e50;
        }}
        
        /* Grid Layouts */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}
        
        .card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .card h3 {{
            color: {colors['primary']};
            margin-bottom: 15px;
            font-size: 1.3rem;
        }}
        
        /* Testimonials */
        .testimonial {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .testimonial-text {{
            font-size: 1.1rem;
            font-style: italic;
            margin-bottom: 20px;
            color: #555;
        }}
        
        .testimonial-author {{
            font-weight: 600;
            color: {colors['primary']};
        }}
        
        /* Pricing */
        .pricing-card {{
            background: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            max-width: 400px;
            margin: 50px auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .price {{
            font-size: 3rem;
            color: {colors['primary']};
            font-weight: bold;
            margin: 20px 0;
        }}
        
        .price-features {{
            list-style: none;
            margin: 20px 0;
        }}
        
        .price-features li {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        
        /* Contact */
        .contact {{
            background: #2c3e50;
            color: white;
            text-align: center;
        }}
        
        .contact .section-title {{
            color: white;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            
            .section-title {{
                font-size: 2rem;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>{hero['headline']}</h1>
            <p>{hero['subheadline']}</p>
            <a href="#contact" class="cta-button">{hero['cta_button']}</a>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{features['section_title']}</h2>
            <div class="grid">"""

        # Add feature cards
        for feature in features['features_list']:
            html += f"""
                <div class="card">
                    <h3>{feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Benefits Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{benefits['section_title']}</h2>
            <div class="grid">"""

        # Add benefits
        for benefit in benefits['benefits_list']:
            html += f"""
                <div class="card">
                    <h3>✓</h3>
                    <p>{benefit}</p>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{testimonials['section_title']}</h2>
            <div class="grid">"""

        # Add testimonials
        for testimonial in testimonials['testimonials']:
            html += f"""
                <div class="testimonial">
                    <div class="testimonial-text">"{testimonial['text']}"</div>
                    <div class="testimonial-author">- {testimonial['name']}, {testimonial['role']}</div>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{pricing['section_title']}</h2>
            <div class="pricing-card">
                <div class="price">{pricing['price']}</div>
                <ul class="price-features">"""

        # Add pricing features
        for feature in pricing['features']:
            html += f"<li>{feature}</li>"

        html += f"""
                </ul>
                <a href="#contact" class="cta-button">Choose Plan</a>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section contact">
        <div class="container">
            <h2 class="section-title">{contact['section_title']}</h2>
            <p style="font-size: 1.2rem; margin-bottom: 30px;">{contact['cta_text']}</p>
            <a href="mailto:{contact['contact_info'].split(': ')[1]}" class="cta-button">{contact['cta_button']}</a>
            <br><br>
            <p>{contact['contact_info']}</p>
        </div>
    </section>
</body>
</html>"""

        return html
    
    def generate_website(self, product_name: str) -> Dict[str, Any]:
        """Main function: Generate complete website from product name"""
        try:
            print(f"🔍 Analyzing product: {product_name}")
            analysis = self.analyze_product(product_name)
            
            print(f"📝 Generating content for: {product_name}")
            content = self.generate_content(analysis)
            
            print(f"🎨 Creating HTML website for: {product_name}")
            html = self.generate_html(analysis, content)
            
            return {
                "success": True,
                "product_name": product_name,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis,
                "content": content,
                "html": html,
                "generation_method": "Simple Template Engine"
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
        
        # Save HTML file
        html_file = os.path.join(site_dir, "index.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(result["html"])
        
        # Save metadata
        metadata = {
            "product_name": result["product_name"],
            "timestamp": result["timestamp"],
            "generation_method": result.get("generation_method"),
            "analysis": result.get("analysis"),
            "content": result.get("content")
        }
        
        metadata_file = os.path.join(site_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return site_dir

def demo():
    """Demo the simple site generator"""
    generator = SimpleSiteGenerator()
    
    test_products = [
        "Smart Coffee Maker",
        "EcoFit Yoga Mat", 
        "ProCode Text Editor",
        "Gourmet Pizza Restaurant",
        "Luxury Fashion Boutique"
    ]
    
    print("🎯 SIMPLE SITE GENERATOR DEMO")
    print("=" * 50)
    
    for product in test_products:
        print(f"\n🚀 Generating site for: {product}")
        result = generator.generate_website(product)
        
        if result["success"]:
            site_dir = generator.save_website(result)
            print(f"✅ Success! Saved to: {site_dir}")
            print(f"🌐 Open: {os.path.join(site_dir, 'index.html')}")
        else:
            print(f"❌ Failed: {result.get('error')}")
        
        print("-" * 30)

if __name__ == "__main__":
    demo() 