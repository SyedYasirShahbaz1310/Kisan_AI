# Hugging Face Spaces Deployment Guide

This guide will help you deploy the Kisan AI Assistant on Hugging Face Spaces using Docker.

## Prerequisites

- A Hugging Face account (create one at https://huggingface.co/join)
- Your Kisan AI repository with the Dockerfile

## Deployment Steps

### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `kisan-ai-assistant` (or your preferred name)
   - **License**: Choose appropriate license
   - **Select the Space SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free tier) or upgrade if needed

### 2. Clone Your Space Repository

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant
cd kisan-ai-assistant
```

### 3. Copy Files to Space Repository

Copy all the necessary files from your Kisan AI repository:

```bash
# Copy application files
cp /path/to/Kisan_AI/Dockerfile .
cp /path/to/Kisan_AI/app.py .
cp /path/to/Kisan_AI/kisan_assistant.py .
cp /path/to/Kisan_AI/index_knowledge.py .
cp /path/to/Kisan_AI/knowledge_watcher.py .
cp /path/to/Kisan_AI/requirements.txt .
cp /path/to/Kisan_AI/.dockerignore .

# Copy static files if they exist
cp -r /path/to/Kisan_AI/static/ ./static/ 2>/dev/null || :

# Create knowledge directory
mkdir -p knowledge/docs
```

### 4. Add Your Knowledge Sources

Add your verified Pakistan agriculture documents to the `knowledge/docs/` directory:

```bash
# Copy your verified sources
cp your_verified_sources/* knowledge/docs/
```

### 5. Commit and Push to Hugging Face

```bash
git add .
git commit -m "Initial deployment of Kisan AI Assistant"
git push
```

### 6. Wait for Build

- Hugging Face will automatically build your Docker container
- This may take 5-10 minutes depending on dependencies
- You can monitor the build progress in the Space's "Logs" tab

### 7. Access Your App

Once built, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant
```

## Environment Variables (Optional)

You can set environment variables in your Space settings:

1. Go to your Space settings
2. Click on "Variables and secrets"
3. Add variables:
   - `PORT`: 7860 (default for Hugging Face)
   - `DEBUG`: 0
   - `AUTO_WATCH`: 0

## Updating Your Space

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push
```

Hugging Face will automatically rebuild and redeploy your Space.

## Troubleshooting

### Space Not Starting

- Check the "Logs" tab for build errors
- Ensure all dependencies in `requirements.txt` are compatible
- Verify the Dockerfile is correct

### Application Not Responding

- Make sure the app is listening on `0.0.0.0:7860`
- Check that `HOST=0.0.0.0` and `PORT=7860` are set correctly

### Out of Memory

- Upgrade to a better hardware tier in Space settings
- Or optimize your model/dependencies to use less memory

### No Answers from Assistant

- Ensure you've added verified knowledge sources to `knowledge/docs/`
- The app needs at least one document to provide answers
- Check the indexing by viewing logs

## Local Testing with Docker

Before deploying to Hugging Face, test locally:

```bash
# Build the Docker image
docker build -t kisan-ai .

# Run the container
docker run -p 7860:7860 kisan-ai

# Access at http://localhost:7860
```

## Resource Requirements

- **Minimum**: CPU Basic (free tier) - 2 vCPUs, 16 GB RAM
- **Recommended**: CPU Upgrade - for better performance with larger knowledge bases

## Support

For issues:
- Check Hugging Face Spaces documentation: https://huggingface.co/docs/hub/spaces
- Review your Space logs for errors
- Ensure your Dockerfile and dependencies are correct

---

**Note**: The free tier on Hugging Face Spaces may have limitations on uptime and resources. Consider upgrading for production use.
