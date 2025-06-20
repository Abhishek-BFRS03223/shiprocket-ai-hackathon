#!/usr/bin/env python3
"""
Enhanced AI Website Generator with Real Images and Dynamic Sections
Generates unique, professional websites with product-specific content and images
"""

import os
import sys
import json
import re
import random
import requests
from datetime import datetime

class EnhancedSiteGenerator:
    def __init__(self):
        self.output_dir = "generated_sites"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Enhanced category mapping with specific sections
        self.categories = {
            'technology': {
                'keywords': ['smart', 'ai', 'tech', 'app', 'software', 'digital', 'cyber', 'robot', 'drone', 'gadget', 'device', 'electronic', 'computer', 'mobile', 'tablet', 'laptop', 'camera', 'headphone', 'speaker'],
                'color_scheme': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                'sections': ['hero', 'features', 'specifications', 'gallery', 'reviews', 'pricing', 'demo'],
                'images': {
                    'hero': 'technology/gadgets',
                    'features': 'technology/innovation',
                    'gallery': 'technology/devices'
                }
            },
            'food_beverage': {
                'keywords': ['food', 'drink', 'coffee', 'tea', 'restaurant', 'cafe', 'kitchen', 'recipe', 'meal', 'pizza', 'burger', 'cake', 'wine', 'beer', 'juice', 'bakery', 'chef', 'dining'],
                'color_scheme': ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3'],
                'sections': ['hero', 'menu', 'about', 'gallery', 'reviews', 'location', 'contact'],
                'images': {
                    'hero': 'food/cuisine',
                    'menu': 'food/dishes',
                    'gallery': 'food/restaurant'
                }
            },
            'fashion': {
                'keywords': ['fashion', 'clothing', 'style', 'dress', 'shirt', 'pants', 'shoes', 'bag', 'accessory', 'jewelry', 'watch', 'boutique', 'designer', 'trend', 'outfit', 'apparel'],
                'color_scheme': ['#ff6b6b', '#ffd93d', '#6bcf7f', '#4834d4'],
                'sections': ['hero', 'collections', 'featured', 'lookbook', 'about', 'contact'],
                'images': {
                    'hero': 'fashion/models',
                    'collections': 'fashion/clothing',
                    'lookbook': 'fashion/style'
                }
            },
            'health_wellness': {
                'keywords': ['health', 'wellness', 'fitness', 'yoga', 'gym', 'medical', 'therapy', 'nutrition', 'vitamin', 'supplement', 'exercise', 'workout', 'spa', 'massage'],
                'color_scheme': ['#55a3ff', '#17c0eb', '#f8b500', '#7bed9f'],
                'sections': ['hero', 'services', 'benefits', 'testimonials', 'experts', 'contact'],
                'images': {
                    'hero': 'health/wellness',
                    'services': 'health/fitness',
                    'benefits': 'health/lifestyle'
                }
            },
            'business': {
                'keywords': ['business', 'corporate', 'company', 'service', 'consulting', 'professional', 'office', 'team', 'solution', 'agency', 'marketing', 'finance'],
                'color_scheme': ['#2c3e50', '#3498db', '#e74c3c', '#f39c12'],
                'sections': ['hero', 'services', 'about', 'team', 'portfolio', 'testimonials', 'contact'],
                'images': {
                    'hero': 'business/office',
                    'services': 'business/team',
                    'portfolio': 'business/success'
                }
            },
            'general': {
                'keywords': [],
                'color_scheme': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                'sections': ['hero', 'about', 'features', 'gallery', 'contact'],
                'images': {
                    'hero': 'abstract/modern',
                    'features': 'abstract/design',
                    'gallery': 'abstract/creative'
                }
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

    def get_unsplash_image(self, query, width=1200, height=600):
        """Get image from Unsplash API (free tier)"""
        try:
            # Using Unsplash Source API (no API key required)
            url = f"https://source.unsplash.com/{width}x{height}/?{query}"
            return url
        except:
            # Fallback to placeholder
            return f"https://via.placeholder.com/{width}x{height}/667eea/ffffff?text={query.replace('/', '+')}"

    def get_pexels_image(self, query, width=1200, height=600):
        """Alternative image source"""
        # Using Lorem Picsum with seed for consistency
        seed = abs(hash(query)) % 1000
        return f"https://picsum.photos/seed/{seed}/{width}/{height}"

    def generate_dynamic_content(self, product_name, category):
        """Generate dynamic content based on product and category"""
        content = {
            'title': product_name,
            'tagline': self.generate_tagline(product_name, category),
            'description': self.generate_description(product_name, category),
            'features': self.generate_features(product_name, category),
            'sections': self.generate_sections(product_name, category)
        }
        return content

    def generate_tagline(self, product_name, category):
        """Generate category-specific taglines"""
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
        
        return random.choice(taglines.get(category, [f"Discover the Power of {product_name}"]))

    def generate_description(self, product_name, category):
        """Generate category-specific descriptions"""
        descriptions = {
            'technology': f"{product_name} represents the pinnacle of technological innovation, designed to enhance your digital experience with cutting-edge features and intuitive functionality.",
            'food_beverage': f"At {product_name}, we're passionate about creating exceptional culinary experiences that bring people together through the love of great food and drink.",
            'fashion': f"{product_name} is where contemporary style meets timeless elegance, offering premium fashion pieces that express your unique personality.",
            'health_wellness': f"{product_name} is dedicated to empowering your wellness journey with proven solutions that promote health, vitality, and overall well-being.",
            'business': f"{product_name} delivers professional excellence through innovative business solutions tailored to meet your specific needs and drive success."
        }
        
        return descriptions.get(category, f"Discover the exceptional quality and innovation that defines {product_name}.")

    def generate_features(self, product_name, category):
        """Generate category-specific features"""
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
        
        return features.get(category, ["Quality", "Innovation", "Excellence", "Reliability", "Value", "Support"])

    def generate_sections(self, product_name, category):
        """Generate category-specific sections with content"""
        category_data = self.categories.get(category, self.categories['general'])
        sections = {}
        
        for section in category_data['sections']:
            if section == 'hero':
                sections[section] = {
                    'title': self.generate_tagline(product_name, category),
                    'subtitle': self.generate_description(product_name, category),
                    'cta': 'Get Started Today',
                    'image': self.get_unsplash_image(category_data['images']['hero'], 1200, 600)
                }
            elif section == 'features':
                sections[section] = {
                    'title': 'Why Choose Us?',
                    'items': self.generate_features(product_name, category),
                    'image': self.get_unsplash_image(category_data['images'].get('features', 'abstract/design'), 800, 500)
                }
            elif section == 'menu':
                sections[section] = {
                    'title': 'Our Menu',
                    'items': [
                        "Signature Dishes", "Fresh Beverages", "Artisan Desserts",
                        "Seasonal Specials", "Healthy Options", "Chef's Recommendations"
                    ],
                    'image': self.get_unsplash_image(category_data['images'].get('menu', 'food/dishes'), 800, 500)
                }
            elif section == 'services':
                sections[section] = {
                    'title': 'Our Services',
                    'items': self.generate_features(product_name, category),
                    'image': self.get_unsplash_image(category_data['images'].get('services', 'business/service'), 800, 500)
                }
            elif section == 'collections':
                sections[section] = {
                    'title': 'Our Collections',
                    'items': [
                        "Spring Collection", "Summer Essentials", "Autumn Trends",
                        "Winter Warmth", "Limited Edition", "Designer Picks"
                    ],
                    'image': self.get_unsplash_image(category_data['images'].get('collections', 'fashion/clothing'), 800, 500)
                }
            elif section == 'gallery':
                sections[section] = {
                    'title': 'Gallery',
                    'images': [
                        self.get_pexels_image(f"{category}/1", 400, 300),
                        self.get_pexels_image(f"{category}/2", 400, 300),
                        self.get_pexels_image(f"{category}/3", 400, 300),
                        self.get_pexels_image(f"{category}/4", 400, 300)
                    ]
                }
            # Add default section handling
            else:
                sections[section] = {
                    'title': section.replace('_', ' ').title(),
                    'content': f"Discover amazing {section.replace('_', ' ')} at {product_name}."
                }
        
        return sections

    def generate_enhanced_html(self, product_name, category, content):
        """Generate enhanced HTML with dynamic sections"""
        category_data = self.categories.get(category, self.categories['general'])
        colors = category_data['color_scheme']
        
        # Get the first section with items (features, menu, services, collections)
        main_section_key = None
        main_section = None
        for section_key, section_data in content['sections'].items():
            if isinstance(section_data, dict) and 'items' in section_data:
                main_section_key = section_key
                main_section = section_data
                break
        
        # Fallback if no section with items found
        if not main_section:
            main_section_key = 'features'
            main_section = {
                'title': 'Why Choose Us?',
                'items': content['features']
            }
        
        # Enhanced CSS with animations and modern design
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
            
            /* Hero Section */
            .hero {{
                background: linear-gradient(135deg, {colors[0]}, {colors[1]});
                color: white;
                padding: 120px 0 80px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .hero::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('{content['sections']['hero']['image']}') center/cover;
                opacity: 0.3;
                z-index: 0;
            }}
            
            .hero-content {{
                position: relative;
                z-index: 1;
            }}
            
            .hero h1 {{
                font-size: 3.5rem;
                margin-bottom: 1rem;
                animation: fadeInUp 1s ease;
            }}
            
            .hero p {{
                font-size: 1.2rem;
                margin-bottom: 2rem;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                animation: fadeInUp 1s ease 0.2s both;
            }}
            
            .cta-button {{
                display: inline-block;
                background: linear-gradient(45deg, {colors[2]}, {colors[3]});
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                transition: all 0.3s ease;
                animation: fadeInUp 1s ease 0.4s both;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            
            .cta-button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            }}
            
            /* Main Section (Features/Menu/Services/Collections) */
            .main-section {{
                padding: 80px 0;
                background: #f8f9fa;
            }}
            
            .section-title {{
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 3rem;
                color: #333;
            }}
            
            .items-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }}
            
            .item-card {{
                background: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border: 1px solid #e9ecef;
            }}
            
            .item-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            }}
            
            .item-icon {{
                width: 60px;
                height: 60px;
                background: linear-gradient(45deg, {colors[0]}, {colors[1]});
                border-radius: 50%;
                margin: 0 auto 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                color: white;
            }}
            
            /* Gallery Section */
            .gallery {{
                padding: 80px 0;
                background: white;
            }}
            
            .gallery-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin-top: 3rem;
            }}
            
            .gallery-item {{
                position: relative;
                overflow: hidden;
                border-radius: 15px;
                aspect-ratio: 4/3;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .gallery-item:hover {{
                transform: scale(1.05);
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
            
            /* Testimonials */
            .testimonials {{
                padding: 80px 0;
                background: linear-gradient(135deg, {colors[0]}, {colors[1]});
                color: white;
            }}
            
            .testimonial-card {{
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                backdrop-filter: blur(10px);
                margin: 0 auto;
                max-width: 600px;
            }}
            
            /* Footer */
            .footer {{
                background: #2c3e50;
                color: white;
                padding: 40px 0;
                text-align: center;
            }}
            
            .footer-content {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }}
            
            .footer-section h3 {{
                margin-bottom: 1rem;
                color: {colors[2]};
            }}
            
            .footer-section a {{
                color: #bdc3c7;
                text-decoration: none;
                transition: color 0.3s ease;
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
                
                .items-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .gallery-grid {{
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                }}
            }}
        </style>
        """
        
        # Generate dynamic HTML structure
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']} - {content['tagline']}</title>
    <meta name="description" content="{content['description']}">
    {css}
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <a href="#" class="logo">{product_name}</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#{main_section_key}">{main_section['title']}</a></li>
                <li><a href="#gallery">Gallery</a></li>
                <li><a href="#testimonials">Reviews</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>{content['sections']['hero']['title']}</h1>
                <p>{content['sections']['hero']['subtitle']}</p>
                <a href="#{main_section_key}" class="cta-button">{content['sections']['hero']['cta']}</a>
            </div>
        </div>
    </section>

    <!-- Main Section (Features/Menu/Services/Collections) -->
    <section id="{main_section_key}" class="main-section">
        <div class="container">
            <h2 class="section-title">{main_section['title']}</h2>
            <div class="items-grid">
"""
        
        # Add item cards dynamically
        for i, item in enumerate(main_section['items']):
            icons = ['🚀', '⭐', '💎', '🔥', '⚡', '🎯', '🍽️', '☕', '🎨', '💪', '🏆', '🌟']
            html += f"""
                <div class="item-card">
                    <div class="item-icon">{icons[i % len(icons)]}</div>
                    <h3>{item}</h3>
                    <p>Experience the best in class {item.lower()} designed for your needs.</p>
                </div>
"""
        
        html += f"""
            </div>
        </div>
    </section>

    <!-- Gallery Section -->
    <section id="gallery" class="gallery">
        <div class="container">
            <h2 class="section-title">Gallery</h2>
            <div class="gallery-grid">
"""
        
        # Add gallery images if available
        if 'gallery' in content['sections'] and 'images' in content['sections']['gallery']:
            for img_url in content['sections']['gallery']['images']:
                html += f"""
                    <div class="gallery-item">
                        <img src="{img_url}" alt="{product_name} Gallery" loading="lazy">
                    </div>
"""
        
        html += f"""
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2 class="section-title">What Our Customers Say</h2>
            <div class="testimonial-card">
                <p>"Absolutely amazing experience with {product_name}! The quality exceeded my expectations and the service was outstanding. Highly recommended!"</p>
                <h4>- Sarah Johnson</h4>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer id="contact" class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Contact Us</h3>
                    <p>📧 info@{product_name.lower().replace(' ', '')}.com</p>
                    <p>📞 +1 (555) 123-4567</p>
                </div>
                <div class="footer-section">
                    <h3>Follow Us</h3>
                    <p><a href="#">Facebook</a></p>
                    <p><a href="#">Twitter</a></p>
                    <p><a href="#">Instagram</a></p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <p><a href="#home">Home</a></p>
                    <p><a href="#{main_section_key}">{main_section['title']}</a></p>
                    <p><a href="#gallery">Gallery</a></p>
                </div>
            </div>
            <div style="border-top: 1px solid #34495e; padding-top: 20px; margin-top: 20px;">
                <p>&copy; 2024 {product_name}. All rights reserved. | Generated by AI Site Generator</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Add scroll effect to header
        window.addEventListener('scroll', function() {{
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {{
                header.style.background = 'rgba(0,0,0,0.9)';
            }} else {{
                header.style.background = 'linear-gradient(135deg, {colors[0]}, {colors[1]})';
            }}
        }});
    </script>
</body>
</html>"""
        
        return html

    def generate_site(self, product_name):
        """Generate enhanced website with real images and dynamic content"""
        print(f"🔍 Analyzing product: {product_name}")
        
        # Categorize product
        category = self.categorize_product(product_name)
        print(f"📂 Category detected: {category}")
        
        # Generate dynamic content
        print(f"📝 Generating enhanced content for: {product_name}")
        content = self.generate_dynamic_content(product_name, category)
        
        # Generate HTML
        print(f"🎨 Creating enhanced website with real images for: {product_name}")
        html_content = self.generate_enhanced_html(product_name, category, content)
        
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
            'description': content['description']
        }
        
        metadata_file = os.path.join(site_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Enhanced website generated successfully!")
        return site_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python enhanced_site_generator.py <product_name>")
        return
    
    product_name = ' '.join(sys.argv[1:])
    generator = EnhancedSiteGenerator()
    
    try:
        site_dir = generator.generate_site(product_name)
        print(f"SUCCESS:{site_dir}")
    except Exception as e:
        print(f"ERROR:{str(e)}")

if __name__ == "__main__":
    main() 