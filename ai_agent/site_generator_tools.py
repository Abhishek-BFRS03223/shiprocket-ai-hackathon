"""
Site Generator Tools for One-Click Website Creation
Specialized tools for generating websites from product names
"""

import json
import re
from typing import Dict, Any, List

try:
    from langchain.tools import BaseTool
    from pydantic import BaseModel, Field
except ImportError:
    print("Warning: LangChain not available, creating mock BaseTool")
    class BaseTool:
        name = ""
        description = ""
        def _run(self, *args, **kwargs):
            pass

class ProductAnalysisTool(BaseTool):
    """Analyze product name to extract key attributes and generate content strategy"""
    name = "product_analyzer"
    description = "Analyze a product name to extract category, features, target audience, and content strategy"
    
    def _run(self, product_name: str) -> str:
        """Analyze product and return structured data"""
        try:
            # Mock analysis - in real implementation, this would use AI
            analysis = {
                "product_name": product_name,
                "category": self._categorize_product(product_name),
                "target_audience": self._identify_audience(product_name),
                "key_features": self._extract_features(product_name),
                "color_scheme": self._suggest_colors(product_name),
                "tone": self._suggest_tone(product_name),
                "content_sections": self._suggest_sections(product_name)
            }
            
            return f"Product Analysis Complete:\n{json.dumps(analysis, indent=2)}"
            
        except Exception as e:
            return f"Error analyzing product: {str(e)}"
    
    def _categorize_product(self, name: str) -> str:
        """Categorize product based on name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['app', 'software', 'platform', 'tool', 'system']):
            return "technology"
        elif any(word in name_lower for word in ['food', 'restaurant', 'cafe', 'kitchen', 'recipe']):
            return "food_beverage"
        elif any(word in name_lower for word in ['fashion', 'clothing', 'style', 'wear', 'fashion']):
            return "fashion"
        elif any(word in name_lower for word in ['health', 'fitness', 'wellness', 'medical', 'care']):
            return "health_wellness"
        else:
            return "general_product"
    
    def _identify_audience(self, name: str) -> str:
        """Identify target audience"""
        categories = {
            "technology": "Tech-savvy professionals and early adopters",
            "food_beverage": "Food enthusiasts and families",
            "fashion": "Style-conscious individuals",
            "health_wellness": "Health and wellness focused individuals",
            "general_product": "General consumers"
        }
        category = self._categorize_product(name)
        return categories.get(category, "General consumers")
    
    def _extract_features(self, name: str) -> List[str]:
        """Extract potential features from product name"""
        name_lower = name.lower()
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
            
        return features
    
    def _suggest_colors(self, name: str) -> Dict[str, str]:
        """Suggest color scheme based on product"""
        category = self._categorize_product(name)
        color_schemes = {
            "technology": {"primary": "#007ACC", "secondary": "#F8F9FA", "accent": "#FF6B6B"},
            "food_beverage": {"primary": "#FF8C42", "secondary": "#FFF8DC", "accent": "#228B22"},
            "fashion": {"primary": "#E91E63", "secondary": "#F5F5F5", "accent": "#9C27B0"},
            "health_wellness": {"primary": "#4CAF50", "secondary": "#E8F5E8", "accent": "#2196F3"},
            "general_product": {"primary": "#2196F3", "secondary": "#F5F5F5", "accent": "#FF9800"}
        }
        return color_schemes.get(category, color_schemes["general_product"])
    
    def _suggest_tone(self, name: str) -> str:
        """Suggest content tone"""
        category = self._categorize_product(name)
        tones = {
            "technology": "Professional and innovative",
            "food_beverage": "Warm and inviting",
            "fashion": "Trendy and aspirational",
            "health_wellness": "Caring and trustworthy",
            "general_product": "Friendly and approachable"
        }
        return tones.get(category, "Friendly and approachable")
    
    def _suggest_sections(self, name: str) -> List[str]:
        """Suggest website sections"""
        return [
            "Hero Section",
            "Product Features",
            "Benefits",
            "How It Works",
            "Testimonials",
            "Pricing",
            "Contact/CTA"
        ]


class ContentGeneratorTool(BaseTool):
    """Generate website content based on product analysis"""
    name = "content_generator"
    description = "Generate website content including headlines, descriptions, and copy for each section"
    
    def _run(self, product_analysis: str) -> str:
        """Generate content based on product analysis"""
        try:
            # Parse the analysis
            if "Product Analysis Complete:" in product_analysis:
                analysis_json = product_analysis.split("Product Analysis Complete:\n")[1]
                analysis = json.loads(analysis_json)
            else:
                return "Error: Invalid product analysis format"
            
            content = self._generate_content_sections(analysis)
            return f"Generated Content:\n{json.dumps(content, indent=2)}"
            
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def _generate_content_sections(self, analysis: Dict) -> Dict:
        """Generate content for each section"""
        product_name = analysis.get("product_name", "Product")
        category = analysis.get("category", "general_product")
        tone = analysis.get("tone", "Friendly and approachable")
        features = analysis.get("key_features", [])
        
        content = {
            "hero": {
                "headline": f"Discover {product_name} - Revolutionary Innovation",
                "subheadline": f"Transform your experience with {product_name}",
                "cta_button": "Get Started Today",
                "hero_text": f"Experience the future with {product_name}. Designed for those who demand excellence."
            },
            "features": {
                "section_title": "Why Choose " + product_name,
                "features_list": [
                    {
                        "title": feature,
                        "description": f"Experience {feature.lower()} like never before"
                    } for feature in features[:3]
                ]
            },
            "benefits": {
                "section_title": "Benefits You'll Love",
                "benefits_list": [
                    "Save time and increase efficiency",
                    "Professional results guaranteed", 
                    "Easy to use for everyone"
                ]
            },
            "how_it_works": {
                "section_title": "How It Works",
                "steps": [
                    {"step": 1, "title": "Get Started", "description": "Quick and easy setup"},
                    {"step": 2, "title": "Customize", "description": "Tailor to your needs"},
                    {"step": 3, "title": "Enjoy", "description": "Experience the results"}
                ]
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
                "price": "$99",
                "features": ["All features included", "24/7 support", "30-day guarantee"]
            },
            "contact": {
                "section_title": "Ready to Start?",
                "cta_text": f"Join thousands who love {product_name}",
                "cta_button": "Get " + product_name + " Now",
                "contact_info": "Contact us: hello@" + product_name.lower().replace(" ", "") + ".com"
            }
        }
        
        return content


class HTMLGeneratorTool(BaseTool):
    """Generate complete HTML website with styling"""
    name = "html_generator"
    description = "Generate complete HTML website with CSS styling based on content and design analysis"
    
    def _run(self, content_data: str) -> str:
        """Generate HTML website"""
        try:
            # Parse content data
            if "Generated Content:" in content_data:
                content_json = content_data.split("Generated Content:\n")[1]
                content = json.loads(content_json)
            else:
                return "Error: Invalid content data format"
            
            html = self._generate_html_template(content)
            return f"Generated HTML Website:\n\n{html}"
            
        except Exception as e:
            return f"Error generating HTML: {str(e)}"
    
    def _generate_html_template(self, content: Dict) -> str:
        """Generate complete HTML template"""
        hero = content.get("hero", {})
        features = content.get("features", {})
        benefits = content.get("benefits", {})
        how_it_works = content.get("how_it_works", {})
        testimonials = content.get("testimonials", {})
        pricing = content.get("pricing", {})
        contact = content.get("contact", {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hero.get('headline', 'Product Website')}</title>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .cta-button {{
            background: #ff6b6b;
            color: white;
            padding: 15px 30px;
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
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
        }}
        
        /* Sections */
        .section {{
            padding: 80px 0;
        }}
        
        .section:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .section-title {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 50px;
            color: #2c3e50;
        }}
        
        /* Features Grid */
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}
        
        .feature-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        
        /* Steps */
        .steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}
        
        .step {{
            text-align: center;
            padding: 20px;
        }}
        
        .step-number {{
            background: #667eea;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 0 auto 20px;
        }}
        
        /* Testimonials */
        .testimonials {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}
        
        .testimonial {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
            color: #667eea;
            font-weight: bold;
            margin: 20px 0;
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
                font-size: 2rem;
            }}
            
            .section-title {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>{hero.get('headline', 'Amazing Product')}</h1>
            <p>{hero.get('subheadline', 'Transform your experience')}</p>
            <a href="#contact" class="cta-button">{hero.get('cta_button', 'Get Started')}</a>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{features.get('section_title', 'Features')}</h2>
            <div class="features-grid">"""

        # Add feature cards
        for feature in features.get('features_list', []):
            html += f"""
                <div class="feature-card">
                    <h3>{feature.get('title', 'Feature')}</h3>
                    <p>{feature.get('description', 'Amazing feature description')}</p>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Benefits Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{benefits.get('section_title', 'Benefits')}</h2>
            <div class="features-grid">"""

        # Add benefits
        for benefit in benefits.get('benefits_list', []):
            html += f"""
                <div class="feature-card">
                    <h3>✓</h3>
                    <p>{benefit}</p>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- How It Works Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{how_it_works.get('section_title', 'How It Works')}</h2>
            <div class="steps">"""

        # Add steps
        for step in how_it_works.get('steps', []):
            html += f"""
                <div class="step">
                    <div class="step-number">{step.get('step', '1')}</div>
                    <h3>{step.get('title', 'Step')}</h3>
                    <p>{step.get('description', 'Step description')}</p>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{testimonials.get('section_title', 'Testimonials')}</h2>
            <div class="testimonials">"""

        # Add testimonials
        for testimonial in testimonials.get('testimonials', []):
            html += f"""
                <div class="testimonial">
                    <p>"{testimonial.get('text', 'Great product!')}"</p>
                    <h4>- {testimonial.get('name', 'Customer')}, {testimonial.get('role', 'User')}</h4>
                </div>"""

        html += f"""
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">{pricing.get('section_title', 'Pricing')}</h2>
            <div class="pricing-card">
                <div class="price">{pricing.get('price', '$99')}</div>
                <ul>"""

        # Add pricing features
        for feature in pricing.get('features', []):
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
            <h2 class="section-title">{contact.get('section_title', 'Contact')}</h2>
            <p>{contact.get('cta_text', 'Get in touch with us')}</p>
            <br>
            <a href="mailto:{contact.get('contact_info', 'hello@product.com')}" class="cta-button">{contact.get('cta_button', 'Contact Us')}</a>
        </div>
    </section>
</body>
</html>"""

        return html


class ImageGeneratorTool(BaseTool):
    """Generate image prompts and placeholder images for the website"""
    name = "image_generator"
    description = "Generate image prompts and create placeholder images for website sections"
    
    def _run(self, product_analysis: str) -> str:
        """Generate image specifications and prompts"""
        try:
            if "Product Analysis Complete:" in product_analysis:
                analysis_json = product_analysis.split("Product Analysis Complete:\n")[1]
                analysis = json.loads(analysis_json)
            else:
                return "Error: Invalid product analysis format"
            
            images = self._generate_image_specs(analysis)
            return f"Generated Image Specifications:\n{json.dumps(images, indent=2)}"
            
        except Exception as e:
            return f"Error generating images: {str(e)}"
    
    def _generate_image_specs(self, analysis: Dict) -> Dict:
        """Generate image specifications for each section"""
        product_name = analysis.get("product_name", "Product")
        category = analysis.get("category", "general_product")
        
        images = {
            "hero_image": {
                "prompt": f"Professional hero image for {product_name}, {category} category, modern and clean design",
                "placeholder": f"https://via.placeholder.com/1200x600/667eea/ffffff?text={product_name}+Hero",
                "alt_text": f"{product_name} hero image"
            },
            "feature_icons": [
                {
                    "prompt": f"Icon representing key feature of {product_name}",
                    "placeholder": "https://via.placeholder.com/100x100/007ACC/ffffff?text=⚡",
                    "alt_text": "Feature icon"
                }
            ],
            "product_demo": {
                "prompt": f"Product demonstration image for {product_name}",
                "placeholder": f"https://via.placeholder.com/800x500/f8f9fa/333333?text={product_name}+Demo",
                "alt_text": f"{product_name} demonstration"
            },
            "testimonial_avatars": [
                {
                    "placeholder": "https://via.placeholder.com/80x80/ddd/333?text=👤",
                    "alt_text": "Customer avatar"
                }
            ]
        }
        
        return images


def get_site_generator_tools():
    """Get all site generator tools"""
    return [
        ProductAnalysisTool(),
        ContentGeneratorTool(), 
        HTMLGeneratorTool(),
        ImageGeneratorTool()
    ] 