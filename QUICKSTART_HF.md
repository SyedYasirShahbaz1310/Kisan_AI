# 🚀 Quick Start: Deploy to Hugging Face Spaces

This is a quick reference guide to deploy Kisan AI to Hugging Face Spaces in minutes.

## Prerequisites

- Hugging Face account (free): https://huggingface.co/join
- Git installed on your computer
- Your Kisan AI repository files

## 5-Minute Deployment

### Step 1: Create a Space (2 minutes)

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Owner**: Your username
   - **Space name**: `kisan-ai-assistant` (or your choice)
   - **License**: Apache 2.0 (recommended)
   - **Select SDK**: **Docker** ⚠️ Important!
   - **Space hardware**: CPU basic (free tier)
4. Click **"Create Space"**

### Step 2: Clone Your Space (1 minute)

```bash
# Replace YOUR_USERNAME with your Hugging Face username
git clone https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant
cd kisan-ai-assistant
```

### Step 3: Copy Files (1 minute)

Copy these files from your Kisan_AI repository:

```bash
# Copy from your Kisan_AI directory
cp /path/to/Kisan_AI/Dockerfile .
cp /path/to/Kisan_AI/app.py .
cp /path/to/Kisan_AI/kisan_assistant.py .
cp /path/to/Kisan_AI/index_knowledge.py .
cp /path/to/Kisan_AI/knowledge_watcher.py .
cp /path/to/Kisan_AI/requirements.txt .
cp /path/to/Kisan_AI/.dockerignore .
cp /path/to/Kisan_AI/.env.example .
cp -r /path/to/Kisan_AI/static .

# Create knowledge directory
mkdir -p knowledge/docs
```

Or use this one-liner (adjust path):

```bash
cd YOUR_SPACE_DIR && cp -r /path/to/Kisan_AI/{Dockerfile,app.py,kisan_assistant.py,index_knowledge.py,knowledge_watcher.py,requirements.txt,.dockerignore,.env.example,static} . && mkdir -p knowledge/docs
```

### Step 4: Push to Hugging Face (1 minute)

```bash
git add .
git commit -m "Initial deployment of Kisan AI Assistant"
git push
```

### Step 5: Wait for Build (5-10 minutes)

- Hugging Face will automatically build your Docker container
- Monitor progress at: `https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant`
- Click on **"Logs"** tab to see build progress

### Step 6: Access Your App! ✅

Once built, your app is live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant
```

## What You Get

✅ Live Flask web app
✅ Web UI at `/static/ui.html`
✅ API endpoint at `/ask`
✅ Automatic HTTPS
✅ Free hosting (basic tier)

## Add Knowledge Sources (Optional)

To get real answers instead of the placeholder:

1. Add your verified Pakistan agriculture documents to `knowledge/docs/`
2. Commit and push:
   ```bash
   git add knowledge/docs/
   git commit -m "Add knowledge sources"
   git push
   ```
3. Hugging Face will rebuild automatically

## Testing Your Deployment

### Test the UI
Visit: `https://huggingface.co/spaces/YOUR_USERNAME/kisan-ai-assistant`

### Test the API
```bash
curl -X POST https://YOUR_USERNAME-kisan-ai-assistant.hf.space/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Wheat rust ka solution kya hai?", "language": "auto"}'
```

## Common Issues

### Build Failed
- Check the **Logs** tab in your Space
- Verify all files were copied correctly
- Check requirements.txt is complete

### App Not Loading
- Wait for build to complete (can take 10 minutes)
- Check that SDK is set to "Docker"
- Restart the Space (Settings → Restart)

### No Answers
- Add knowledge sources to `knowledge/docs/`
- The sample placeholder won't give real answers

### Out of Memory
- Upgrade to a better hardware tier:
  - Go to Settings → Change hardware
  - Choose CPU Upgrade or higher

## Environment Variables (Optional)

Set in Space Settings → Variables:

```
PORT=7860
DEBUG=0
AUTO_WATCH=0
```

## Updating Your App

To update code or add knowledge:

```bash
# Make changes to files
git add .
git commit -m "Update: description"
git push
```

Hugging Face automatically rebuilds.

## Cost

- **Free tier**: CPU basic (2 vCPU, 16 GB RAM)
- **Limitations**: May sleep after inactivity, limited resources
- **Upgrades available**: For production use

## Files Required

Minimum files needed:
- ✅ Dockerfile
- ✅ app.py
- ✅ kisan_assistant.py
- ✅ index_knowledge.py
- ✅ knowledge_watcher.py
- ✅ requirements.txt
- ✅ static/ui.html
- ✅ .dockerignore
- ✅ .env.example

## Next Steps

1. ✅ Deploy (you're done!)
2. 📚 Add verified knowledge sources
3. 🎨 Customize UI (edit static/ui.html)
4. 🔧 Configure environment variables
5. 📈 Monitor usage and upgrade if needed

## Full Documentation

For detailed guides, see:
- `HUGGINGFACE_DEPLOYMENT.md` - Complete HF deployment guide
- `DOCKER_DEPLOYMENT.md` - Docker deployment guide
- `DEPLOYMENT_SUMMARY.md` - Summary of all deployment files

## Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Check Space logs for errors
- Verify Docker SDK is selected
- Review requirements.txt compatibility

---

**That's it!** Your Kisan AI Assistant is now live on Hugging Face Spaces! 🎉

Share your Space URL with farmers and agricultural workers to help them with verified Pakistan agriculture information.
