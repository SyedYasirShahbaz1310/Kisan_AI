#!/bin/bash
# Quick Hugging Face Deployment Script
# This script helps you prepare and deploy to Hugging Face Spaces

set -e

echo "🌾 Kisan AI - Hugging Face Deployment Helper"
echo "============================================="
echo ""

# Check if HF_USERNAME is provided
if [ -z "$1" ]; then
    echo "Usage: ./deploy_hf.sh YOUR_HF_USERNAME [SPACE_NAME]"
    echo ""
    echo "Example: ./deploy_hf.sh johndoe kisan-ai-assistant"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME=${2:-kisan-ai-assistant}

echo "📋 Configuration:"
echo "  Username: $HF_USERNAME"
echo "  Space Name: $SPACE_NAME"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    exit 1
fi

echo "📝 Steps to deploy:"
echo ""
echo "1. Create a new Space on Hugging Face:"
echo "   - Go to https://huggingface.co/spaces"
echo "   - Click 'Create new Space'"
echo "   - Name: $SPACE_NAME"
echo "   - SDK: Docker"
echo "   - Click 'Create Space'"
echo ""
echo "2. Clone your space repository:"
echo "   git clone https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo "   cd $SPACE_NAME"
echo ""
echo "3. Copy files from Kisan_AI to your space:"
echo "   cp -r $(pwd)/Dockerfile $(pwd)/app.py $(pwd)/kisan_assistant.py \\"
echo "         $(pwd)/index_knowledge.py $(pwd)/knowledge_watcher.py \\"
echo "         $(pwd)/requirements.txt $(pwd)/.dockerignore \\"
echo "         $(pwd)/static ../\$SPACE_NAME/"
echo ""
echo "4. Add your knowledge sources:"
echo "   mkdir -p ../\$SPACE_NAME/knowledge/docs"
echo "   # Copy your verified Pakistan agriculture documents here"
echo ""
echo "5. Commit and push:"
echo "   cd ../\$SPACE_NAME"
echo "   git add ."
echo "   git commit -m 'Initial deployment of Kisan AI Assistant'"
echo "   git push"
echo ""
echo "6. Wait for build (5-10 minutes)"
echo "   Monitor at: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "✅ Your app will be available at:"
echo "   https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "📚 For detailed instructions, see HUGGINGFACE_DEPLOYMENT.md"
