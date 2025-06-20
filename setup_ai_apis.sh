#!/bin/bash
# AI Image Generation API Setup Script

echo "🎨 AI Image Generation API Setup"
echo "================================="

# Create environment file
cat > .env << 'EOF'
# AI Image Generation API Keys
# Uncomment and add your API keys below

# OpenAI DALL-E 3 (Premium Quality)
# Cost: ~$0.04 per image
# Get key from: https://platform.openai.com/api-keys
# OPENAI_API_KEY=your_openai_api_key_here

# Stability AI (Good Quality)
# Cost: ~$0.05 per image  
# Get key from: https://platform.stability.ai/account/keys
# STABILITY_API_KEY=your_stability_api_key_here

# Hugging Face (Free Tier Available)
# Get token from: https://huggingface.co/settings/tokens
# HUGGINGFACE_TOKEN=your_huggingface_token_here

EOF

echo "✅ Created .env file"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. 🔑 Get API Keys:"
echo "   • OpenAI DALL-E: https://platform.openai.com/api-keys"
echo "   • Stability AI: https://platform.stability.ai/account/keys"
echo "   • Hugging Face: https://huggingface.co/settings/tokens (FREE)"
echo ""
echo "2. ✏️ Edit .env file and add your API keys"
echo ""
echo "3. 🚀 Load environment variables:"
echo "   source .env"
echo ""
echo "4. 🧪 Test image generation:"
echo "   python3 ai_image_generator.py 'Smart Watch' dalle"
echo ""
echo "💡 RECOMMENDATIONS:"
echo "• Start with Hugging Face (free tier)"
echo "• Use OpenAI DALL-E for best quality"
echo "• Stability AI for good balance of cost/quality"
echo ""
echo "💰 ESTIMATED COSTS:"
echo "• Hugging Face: FREE (with limits)"
echo "• OpenAI DALL-E: $0.04 per image"
echo "• Stability AI: $0.05 per image"
echo "• Full website (10 images): ~$0.40-0.50" 