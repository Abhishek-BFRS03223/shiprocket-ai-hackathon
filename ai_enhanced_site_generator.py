#!/usr/bin/env python3
"""
AI-Enhanced Site Generator with Custom Image Generation
Combines website generation with AI-generated custom images
"""

import os
import sys
import json
import re
import random
from datetime import datetime
from ai_image_generator import AIImageGenerator

class AIEnhancedSiteGenerator:
    def __init__(self):
        self.output_dir = "generated_sites"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize AI image generator
        self.image_generator = AIImageGenerator()
        
        # Enhanced category mapping
        self.categories = {
            'technology': {
                'keywords': ['smart', 'ai', 'tech', 'app', 'software', 'digital', 'cyber', 'robot', 'drone', 'gadget', 'device', 'electronic', 'computer', 'mobile', 'tablet', 'laptop', 'camera', 'headphone', 'speaker'],
                'color_scheme': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                'sections': ['hero', 'features', 'specifications', 'gallery', 'reviews', 'pricing', 'demo']
            },
            'food_beverage': {
                'keywords': ['food', 'drink', 'coffee', 'tea', 'restaurant', 'cafe', 'kitchen', 'recipe', 'meal', 'pizza', 'burger', 'cake', 'wine', 'beer', 'juice', 'bakery', 'chef', 'dining'],
                'color_scheme': ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3'],
                'sections': ['hero', 'menu', 'about', 'gallery', 'reviews', 'location', 'contact']
            },
            'fashion': {
                'keywords': ['fashion', 'clothing', 'style', 'dress', 'shirt', 'pants', 'shoes', 'bag', 'accessory', 'jewelry', 'watch', 'boutique', 'designer', 'trend', 'outfit', 'apparel'],
                'color_scheme': ['#ff6b6b', '#ffd93d', '#6bcf7f', '#4834d4'],
                'sections': ['hero', 'collections', 'featured', 'lookbook', 'about', 'contact']
            },
            'health_wellness': {
                'keywords': ['health', 'wellness', 'fitness', 'yoga', 'gym', 'medical', 'therapy', 'nutrition', 'vitamin', 'supplement', 'exercise', 'workout', 'spa', 'massage'],
                'color_scheme': ['#55a3ff', '#17c0eb', '#f8b500', '#7bed9f'],
                'sections': ['hero', 'services', 'benefits', 'testimonials', 'experts', 'contact']
            },
            'business': {
                'keywords': ['business', 'corporate', 'company', 'service', 'consulting', 'professional', 'office', 'team', 'solution', 'agency', 'marketing', 'finance'],
                'color_scheme': ['#2c3e50', '#3498db', '#e74c3c', '#f39c12'],
                'sections': ['hero', 'services', 'about', 'team', 'portfolio', 'testimonials', 'contact']
            },
            'general': {
                'keywords': [],
                'color_scheme': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                'sections': ['hero', 'about', 'features', 'gallery', 'contact']
            }
        }

    def categorize_product(self, product_name):
        """Enhanced product categorization"""
        product_lower = product_name.lower()
        
        for category, data in self.categories.items():
            if category == 'general':
                continue
            for keyword in data['keywords']:
                if keyword in product_lower:
                    return category
        
        return 'general'

    def generate_dynamic_content(self, product_name, category):
        """Generate dynamic content based on product and category"""
        taglines = {
            'technology': [
                f"Experience the Future with {product_name}",
                f"Innovation Meets Excellence in {product_name}",
                f"Smart Technology for Smart Living"
            ],
            'food_beverage': [
                f"Taste the Difference with {product_name}",
                f"Where Flavor Meets Passion",
                f"Authentic Taste, Unforgettable Experience"
            ],
            'fashion': [
                f"Define Your Style with {product_name}",
                f"Fashion Forward, Always",
                f"Where Elegance Meets Innovation"
            ],
            'health_wellness': [
                f"Transform Your Life with {product_name}",
                f"Your Journey to Better Health Starts Here",
                f"Wellness Redefined"
            ],
            'business': [
                f"Professional Solutions with {product_name}",
                f"Excellence in Every Detail",
                f"Your Success is Our Mission"
            ]
        }
        
        descriptions = {
            'technology': f"{product_name} represents the pinnacle of technological innovation, designed to enhance your digital experience with cutting-edge features and intuitive functionality.",
            'food_beverage': f"At {product_name}, we're passionate about creating exceptional culinary experiences that bring people together through the love of great food and drink.",
            'fashion': f"{product_name} is where contemporary style meets timeless elegance, offering premium fashion pieces that express your unique personality.",
            'health_wellness': f"{product_name} is dedicated to empowering your wellness journey with proven solutions that promote health, vitality, and overall well-being.",
            'business': f"{product_name} delivers professional excellence through innovative business solutions tailored to meet your specific needs and drive success."
        }
        
        features = {
            'technology': [
                "Advanced AI Integration", "Seamless Connectivity", "Intuitive User Interface",
                "Premium Build Quality", "Extended Battery Life", "Smart Automation"
            ],
            'food_beverage': [
                "Fresh Ingredients", "Authentic Recipes", "Expert Chefs",
                "Sustainable Sourcing", "Customizable Options", "Fast Service"
            ],
            'fashion': [
                "Premium Materials", "Timeless Design", "Perfect Fit",
                "Sustainable Fashion", "Exclusive Collections", "Expert Craftsmanship"
            ],
            'health_wellness': [
                "Proven Results", "Natural Ingredients", "Expert Guidance",
                "Personalized Programs", "24/7 Support", "Scientific Backing"
            ],
            'business': [
                "Professional Expertise", "Tailored Solutions", "Proven Track Record",
                "24/7 Support", "Scalable Services", "Competitive Pricing"
            ]
        }
        
        content = {
            'title': product_name,
            'tagline': random.choice(taglines.get(category, [f"Discover the Power of {product_name}"])),
            'description': descriptions.get(category, f"Discover the exceptional quality and innovation that defines {product_name}."),
            'features': features.get(category, ["Quality", "Innovation", "Excellence", "Reliability", "Value", "Support"])
        }
        
        return content

    def generate_enhanced_html_with_ai_images(self, product_name, category, content, ai_images):
        """Generate enhanced HTML with AI-generated images"""
        category_data = self.categories.get(category, self.categories['general'])
        colors = category_data['color_scheme']
        
        # Use AI-generated hero background or fallback
        hero_bg_image = ai_images.get('hero_background', [None])[0] if ai_images.get('hero_background') else 'https://source.unsplash.com/1920x1080/?technology'
        
        # Enhanced CSS with AI images
        css = f"""
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
                overflow-x: hidden;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }}
            
            /* Header Styles */
            .header {{
                background: linear-gradient(135deg, {colors[0]}, {colors[1]});
                color: white;
                padding: 1rem 0;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            
            .nav {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .logo {{
                font-size: 1.8rem;
                font-weight: bold;
                text-decoration: none;
                color: white;
            }}
            
            .nav-links {{
                display: flex;
                list-style: none;
                gap: 2rem;
            }}
            
            .nav-links a {{
                color: white;
                text-decoration: none;
                transition: all 0.3s ease;
            }}
            
            .nav-links a:hover {{
                color: {colors[2]};
                transform: translateY(-2px);
            }}
            
            /* Hero Section with AI Background */
            .hero {{
                background: linear-gradient(135deg, {colors[0]}, {colors[1]});
                color: white;
                padding: 120px 0 80px;
                text-align: center;
                position: relative;
                overflow: hidden;
                min-height: 100vh;
            }}
            
            .hero::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('{hero_bg_image}') center/cover;
                opacity: 0.4;
                z-index: 0;
            }}
            
            .hero-content {{
                position: relative;
                z-index: 1;
                padding-top: 5rem;
            }}
            
            .hero h1 {{
                font-size: 4rem;
                margin-bottom: 1.5rem;
                animation: fadeInUp 1s ease;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
            
            .hero p {{
                font-size: 1.3rem;
                margin-bottom: 2.5rem;
                max-width: 700px;
                margin-left: auto;
                margin-right: auto;
                animation: fadeInUp 1s ease 0.2s both;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }}
            
            .cta-button {{
                display: inline-block;
                background: linear-gradient(45deg, {colors[2]}, {colors[3]});
                color: white;
                padding: 18px 36px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                animation: fadeInUp 1s ease 0.4s both;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            
            .cta-button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            }}
            
            /* Features Section */
            .features {{
                padding: 100px 0;
                background: #f8f9fa;
            }}
            
            .section-title {{
                text-align: center;
                font-size: 3rem;
                margin-bottom: 3rem;
                color: #333;
                font-weight: bold;
            }}
            
            .features-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 2.5rem;
                margin-top: 4rem;
            }}
            
            .feature-card {{
                background: white;
                padding: 2.5rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 15px 40px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border: 1px solid #e9ecef;
                position: relative;
                overflow: hidden;
            }}
            
            .feature-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, {colors[0]}, {colors[1]});
            }}
            
            .feature-card:hover {{
                transform: translateY(-15px);
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            }}
            
            .feature-icon {{
                width: 80px;
                height: 80px;
                background: linear-gradient(45deg, {colors[0]}, {colors[1]});
                border-radius: 50%;
                margin: 0 auto 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                color: white;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}
            
            .feature-card h3 {{
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: #333;
            }}
            
            .feature-card p {{
                color: #666;
                line-height: 1.6;
            }}
            
            /* AI Gallery Section */
            .ai-gallery {{
                padding: 100px 0;
                background: white;
            }}
            
            .gallery-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 4rem;
            }}
            
            .gallery-item {{
                position: relative;
                overflow: hidden;
                border-radius: 20px;
                aspect-ratio: 4/3;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .gallery-item:hover {{
                transform: scale(1.05);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }}
            
            .gallery-item img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: all 0.3s ease;
            }}
            
            .gallery-item:hover img {{
                transform: scale(1.1);
            }}
            
            /* Product Showcase */
            .product-showcase {{
                padding: 100px 0;
                background: linear-gradient(135deg, {colors[0]}, {colors[1]});
                color: white;
            }}
            
            .showcase-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 3rem;
                margin-top: 4rem;
                align-items: center;
            }}
            
            .showcase-image {{
                text-align: center;
            }}
            
            .showcase-image img {{
                max-width: 100%;
                height: auto;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }}
            
            /* Testimonials */
            .testimonials {{
                padding: 100px 0;
                background: #f8f9fa;
            }}
            
            .testimonial-card {{
                background: white;
                padding: 3rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 15px 40px rgba(0,0,0,0.1);
                margin: 0 auto;
                max-width: 700px;
                position: relative;
            }}
            
            .testimonial-card::before {{
                content: '"';
                font-size: 4rem;
                color: {colors[0]};
                position: absolute;
                top: 1rem;
                left: 2rem;
                font-family: serif;
            }}
            
            /* Footer */
            .footer {{
                background: #2c3e50;
                color: white;
                padding: 60px 0 30px;
                text-align: center;
            }}
            
            .footer-content {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 3rem;
                margin-bottom: 3rem;
            }}
            
            .footer-section h3 {{
                margin-bottom: 1.5rem;
                color: {colors[2]};
                font-size: 1.3rem;
            }}
            
            .footer-section a {{
                color: #bdc3c7;
                text-decoration: none;
                transition: color 0.3s ease;
                display: block;
                margin-bottom: 0.5rem;
            }}
            
            .footer-section a:hover {{
                color: {colors[2]};
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
                .hero h1 {{
                    font-size: 2.5rem;
                }}
                
                .nav-links {{
                    display: none;
                }}
                
                .features-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .gallery-grid {{
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                }}
                
                .showcase-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """
        
        # Generate HTML with AI images
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']} - {content['tagline']}</title>
    <meta name="description" content="{content['description']}">
    <meta name="keywords" content="{product_name}, {category}, quality, innovation, professional">
    {css}
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <a href="#" class="logo">{product_name}</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#gallery">Gallery</a></li>
                <li><a href="#testimonials">Reviews</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section with AI Background -->
    <section id="home" class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>{content['tagline']}</h1>
                <p>{content['description']}</p>
                <a href="#features" class="cta-button">Explore Now</a>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
        <div class="container">
            <h2 class="section-title">Why Choose {product_name}?</h2>
            <div class="features-grid">
"""
        
        # Add feature cards
        icons = ['🚀', '⭐', '💎', '🔥', '⚡', '🎯']
        for i, feature in enumerate(content['features']):
            html += f"""
                <div class="feature-card">
                    <div class="feature-icon">{icons[i % len(icons)]}</div>
                    <h3>{feature}</h3>
                    <p>Experience the best in class {feature.lower()} designed to exceed your expectations and deliver outstanding results.</p>
                </div>
"""
        
        html += f"""
            </div>
        </div>
    </section>
"""
        
        # Add Product Showcase if AI images available
        if ai_images.get('product_showcase'):
            html += f"""
    <!-- Product Showcase with AI Images -->
    <section class="product-showcase">
        <div class="container">
            <h2 class="section-title">Experience {product_name}</h2>
            <div class="showcase-grid">
                <div class="showcase-content">
                    <h3>Premium Quality</h3>
                    <p>Discover the exceptional craftsmanship and attention to detail that makes {product_name} the perfect choice for discerning customers.</p>
                </div>
                <div class="showcase-image">
                    <img src="{ai_images['product_showcase'][0]}" alt="{product_name} Showcase" loading="lazy">
                </div>
            </div>
        </div>
    </section>
"""
        
        # Add AI Gallery if images available
        if ai_images.get('gallery_items'):
            html += f"""
    <!-- AI-Generated Gallery -->
    <section id="gallery" class="ai-gallery">
        <div class="container">
            <h2 class="section-title">Gallery</h2>
            <div class="gallery-grid">
"""
            for i, img_path in enumerate(ai_images['gallery_items'][:4]):
                html += f"""
                <div class="gallery-item">
                    <img src="{img_path}" alt="{product_name} Gallery {i+1}" loading="lazy">
                </div>
"""
            html += """
            </div>
        </div>
    </section>
"""
        
        html += f"""
    <!-- Testimonials Section -->
    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2 class="section-title">What Our Customers Say</h2>
            <div class="testimonial-card">
                <p>Absolutely amazing experience with {product_name}! The quality exceeded my expectations and the innovative features have transformed how I work. Highly recommended to anyone looking for excellence!</p>
                <h4>- Sarah Johnson, Verified Customer</h4>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer id="contact" class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Contact Us</h3>
                    <a href="mailto:info@{product_name.lower().replace(' ', '')}.com">📧 info@{product_name.lower().replace(' ', '')}.com</a>
                    <a href="tel:+15551234567">📞 +1 (555) 123-4567</a>
                    <a href="#">📍 123 Innovation Street, Tech City</a>
                </div>
                <div class="footer-section">
                    <h3>Follow Us</h3>
                    <a href="#">Facebook</a>
                    <a href="#">Twitter</a>
                    <a href="#">Instagram</a>
                    <a href="#">LinkedIn</a>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <a href="#home">Home</a>
                    <a href="#features">Features</a>
                    <a href="#gallery">Gallery</a>
                    <a href="#testimonials">Reviews</a>
                </div>
            </div>
            <div style="border-top: 1px solid #34495e; padding-top: 20px; margin-top: 20px;">
                <p>&copy; 2024 {product_name}. All rights reserved. | Powered by AI-Enhanced Site Generator</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Add scroll effect to header
        window.addEventListener('scroll', function() {{
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {{
                header.style.background = 'rgba(0,0,0,0.95)';
                header.style.backdropFilter = 'blur(10px)';
            }} else {{
                header.style.background = 'linear-gradient(135deg, {colors[0]}, {colors[1]})';
                header.style.backdropFilter = 'blur(10px)';
            }}
        }});

        // Gallery image lazy loading and animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);

        // Observe all gallery items and feature cards
        document.querySelectorAll('.gallery-item, .feature-card').forEach(item => {{
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(item);
        }});
    </script>
</body>
</html>"""
        
        return html

    def generate_site_with_ai_images(self, product_name, api_preference="auto", use_ai_images=True):
        """Generate website with AI-generated images"""
        print(f"🎯 Generating AI-enhanced website for: {product_name}")
        
        # Categorize product
        category = self.categorize_product(product_name)
        print(f"📂 Category detected: {category}")
        
        # Generate AI images if enabled and API keys available
        ai_images = {}
        if use_ai_images:
            print("🎨 Generating custom AI images...")
            try:
                image_result = self.image_generator.generate_for_website(product_name, api_preference)
                if image_result['success']:
                    ai_images = image_result['images']
                    print(f"✅ Generated {image_result['total_images']} AI images")
                else:
                    print("⚠️ AI image generation failed, using fallback images")
            except Exception as e:
                print(f"⚠️ AI image generation error: {str(e)}")
                print("🔄 Falling back to standard images")
        
        # Generate dynamic content
        print(f"📝 Generating enhanced content for: {product_name}")
        content = self.generate_dynamic_content(product_name, category)
        
        # Generate HTML with AI images
        print(f"🎨 Creating AI-enhanced website for: {product_name}")
        html_content = self.generate_enhanced_html_with_ai_images(product_name, category, content, ai_images)
        
        # Create site directory
        site_name = re.sub(r'[^a-zA-Z0-9]', '_', product_name.lower())
        site_dir = os.path.join(self.output_dir, site_name)
        os.makedirs(site_dir, exist_ok=True)
        
        # Write HTML file
        html_file = os.path.join(site_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Write metadata
        metadata = {
            'name': product_name,
            'category': category,
            'generated_at': datetime.now().isoformat(),
            'features': content['features'],
            'tagline': content['tagline'],
            'description': content['description'],
            'ai_enhanced': use_ai_images,
            'ai_images_generated': len(ai_images) > 0,
            'total_ai_images': sum(len(imgs) for imgs in ai_images.values()) if ai_images else 0
        }
        
        metadata_file = os.path.join(site_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ AI-enhanced website generated successfully!")
        return site_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_enhanced_site_generator.py <product_name> [api_preference] [--no-ai-images]")
        print("API preferences: dalle, stability, huggingface, auto")
        return
    
    product_name = sys.argv[1]
    api_preference = "auto"
    use_ai_images = True
    
    # Parse arguments
    for arg in sys.argv[2:]:
        if arg in ['dalle', 'stability', 'huggingface', 'auto']:
            api_preference = arg
        elif arg == '--no-ai-images':
            use_ai_images = False
    
    generator = AIEnhancedSiteGenerator()
    
    try:
        site_dir = generator.generate_site_with_ai_images(product_name, api_preference, use_ai_images)
        print(f"SUCCESS:{site_dir}")
    except Exception as e:
        print(f"ERROR:{str(e)}")

if __name__ == "__main__":
    main() 