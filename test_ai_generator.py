#!/usr/bin/env python3
"""
Test script for AI Image Generation
Demonstrates different themes and image types
"""

import os
import time
from ai_image_generator import AIImageGenerator

def test_prompt_generation():
    """Test prompt generation for different themes"""
    print("🧪 TESTING PROMPT GENERATION")
    print("=" * 50)
    
    generator = AIImageGenerator()
    
    test_products = [
        ("Smart Fitness Watch", "technology"),
        ("Artisan Coffee Shop", "food_beverage"),
        ("Designer Handbag", "fashion"),
        ("Yoga Mat", "health_wellness"),
        ("Business Consulting", "business")
    ]
    
    for product, expected_category in test_products:
        print(f"\n📱 Product: {product}")
        category = generator.categorize_product(product)
        print(f"🏷️ Category: {category}")
        
        # Test different image types
        image_types = ['hero_background', 'product_showcase', 'feature_icon', 'gallery_item']
        
        for img_type in image_types:
            prompt = generator.generate_prompt(product, img_type, category, 0)
            print(f"  🎨 {img_type}: {prompt[:100]}...")
        
        print("-" * 30)

def test_image_generation_without_api():
    """Test image generation flow without actual API calls"""
    print("\n🎯 TESTING IMAGE GENERATION FLOW")
    print("=" * 50)
    
    generator = AIImageGenerator()
    
    # Test with mock API keys
    generator.openai_api_key = "test_key"
    generator.stability_api_key = "test_key"
    generator.huggingface_token = "test_token"
    
    print("🔑 API Keys Status:")
    print(f"  OpenAI: {'✅' if generator.openai_api_key else '❌'}")
    print(f"  Stability: {'✅' if generator.stability_api_key else '❌'}")
    print(f"  Hugging Face: {'✅' if generator.huggingface_token else '❌'}")
    
    print("\n📝 Generated Prompts for 'Premium Headphones':")
    category = generator.categorize_product("Premium Headphones")
    
    prompts = []
    for i in range(3):
        prompt = generator.generate_prompt("Premium Headphones", "product_showcase", category, i)
        prompts.append(prompt)
        print(f"  {i+1}. {prompt}")
    
    # Show prompt diversity
    print(f"\n🎨 Prompt Diversity: {len(set(prompts))} unique prompts out of {len(prompts)}")

def demo_theme_variations():
    """Demonstrate different themes and styles"""
    print("\n🎨 THEME VARIATIONS DEMO")
    print("=" * 50)
    
    generator = AIImageGenerator()
    
    themes = generator.themes
    
    for theme_name, theme_data in themes.items():
        print(f"\n🏷️ Theme: {theme_name.upper()}")
        print(f"  🎨 Styles: {', '.join(theme_data['styles'][:3])}...")
        print(f"  🌍 Environments: {', '.join(theme_data['environments'][:3])}...")
        print(f"  💡 Lighting: {', '.join(theme_data['lighting'][:3])}...")
        
        # Generate sample prompt
        sample_prompt = generator.generate_prompt(
            f"Premium {theme_name.replace('_', ' ').title()}", 
            "hero_background", 
            theme_name, 
            0
        )
        print(f"  📝 Sample: {sample_prompt[:80]}...")

def main():
    """Run all tests"""
    print("🚀 AI IMAGE GENERATOR TEST SUITE")
    print("=" * 60)
    
    test_prompt_generation()
    test_image_generation_without_api()
    demo_theme_variations()
    
    print("\n✅ ALL TESTS COMPLETED!")
    print("\n📋 NEXT STEPS:")
    print("1. Run setup script: bash setup_ai_apis.sh")
    print("2. Add your API keys to .env file")
    print("3. Test with real API: python3 ai_image_generator.py 'Smart Watch' huggingface")
    print("4. Generate full website: python3 ai_enhanced_site_generator.py 'Premium Laptop'")

if __name__ == "__main__":
    main() 