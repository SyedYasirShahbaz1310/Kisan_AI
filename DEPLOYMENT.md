# 🚀 Free Deployment Guide - Kisan AI Assistant

This guide shows you how to deploy Kisan AI Assistant for **FREE** on various cloud platforms and get a shareable link.

## 📋 Quick Links to Free Platforms

| Platform | Free Tier | Build Time | Difficulty |
|----------|-----------|------------|------------|
| [Render](https://render.com) | ✅ 750 hours/month | ~5 min | ⭐ Easy |
| [Railway](https://railway.app) | ✅ $5 credit/month | ~3 min | ⭐ Easy |
| [Fly.io](https://fly.io) | ✅ 3 VMs free | ~4 min | ⭐⭐ Medium |
| [Vercel](https://vercel.com) | ✅ Unlimited | ~2 min | ⭐ Easy (Serverless) |
| [Google Cloud Run](https://cloud.google.com/run) | ✅ 2M requests/month | ~5 min | ⭐⭐ Medium |

---

## 🎯 Recommended: Deploy on Render (Easiest & Best Free Tier)

### Step 1: Prepare Your Repository

1. **Push this code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Go to [Render.com](https://render.com)** and sign up (free)

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository:**
   - Select `SyedYasirShahbaz1310/Kisan_AI`

4. **Configure your service:**
   - **Name:** `kisan-ai-assistant` (or your choice)
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT app:app --timeout 120`
   - **Plan:** Select **FREE**

5. **Add Environment Variables:**
   - `AUTO_WATCH` = `0` (disable file watcher for production)
   - `PYTHON_VERSION` = `3.11.0`

6. **Click "Create Web Service"**

7. **Wait 3-5 minutes** for deployment

8. **Get your link:** `https://kisan-ai-assistant.onrender.com` ✅

### Optional: Auto-deployment with render.yaml

The repository includes `render.yaml` for automatic deployment:
- Just connect the repo and Render will use the config automatically
- No manual configuration needed!

---

## 🚂 Alternative: Deploy on Railway

### Step 1: Deploy on Railway

1. **Go to [Railway.app](https://railway.app)** and sign up

2. **Click "New Project" → "Deploy from GitHub repo"**

3. **Select your repository:** `SyedYasirShahbaz1310/Kisan_AI`

4. **Railway auto-detects Python** and uses `Procfile`

5. **Add environment variable:**
   - Go to Variables tab
   - Add: `AUTO_WATCH` = `0`

6. **Click "Deploy"**

7. **Generate domain:**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Get your link: `https://kisan-ai-production.up.railway.app` ✅

**Free Tier:** $5 credit per month (renews monthly)

---

## ✈️ Alternative: Deploy on Fly.io

### Step 1: Install Fly CLI

```bash
# On Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# On macOS/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Deploy

```bash
# Login
fly auth login

# Launch app (from project directory)
fly launch

# Answer prompts:
# - App name: kisan-ai-assistant
# - Region: Choose closest to Pakistan (Mumbai or Singapore)
# - PostgreSQL: No
# - Redis: No

# Deploy
fly deploy
```

**Get your link:** `https://kisan-ai-assistant.fly.dev` ✅

---

## 🔥 Alternative: Deploy on Google Cloud Run

### Step 1: Setup Google Cloud

1. **Go to [Google Cloud Console](https://console.cloud.google.com)**
2. **Enable Cloud Run API**
3. **Install gcloud CLI**

### Step 2: Deploy with Docker

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kisan-ai

# Deploy to Cloud Run
gcloud run deploy kisan-ai-assistant \
  --image gcr.io/YOUR_PROJECT_ID/kisan-ai \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

**Get your link:** `https://kisan-ai-assistant-xxx.a.run.app` ✅

**Free Tier:** 2 million requests/month

---

## 🎨 Alternative: Deploy on Vercel (Serverless)

**Note:** Vercel is for serverless deployment. You'll need to adapt the app for serverless functions.

### Quick Deploy Button

Add this to README.md:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SyedYasirShahbaz1310/Kisan_AI)
```

---

## 📝 After Deployment Checklist

### 1. Test Your Deployment

Visit your deployed URL:
```
https://your-app.platform.com
```

You should see the home page with "Kisan AI Assistant"

### 2. Test the Assistant

Click "Open Assistant" or visit:
```
https://your-app.platform.com/static/ui.html
```

### 3. Test API Endpoint

```bash
curl -X POST https://your-app.platform.com/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Meri wheat pe rust aa gaya hai", "language": "auto"}'
```

### 4. Add Knowledge Base (Important!)

The app currently has only a sample placeholder. To get real agricultural advice:

1. **Collect verified sources** from:
   - PARC (Pakistan Agricultural Research Council)
   - AARI (Ayub Agricultural Research Institute)
   - Punjab Agriculture Department
   - Official agriculture portals

2. **Create JSON files** in `knowledge/docs/`:
   ```json
   {
     "text": "Your verified agricultural content here...",
     "source": "PARC - Wheat Rust Management 2024"
   }
   ```

3. **Commit and push** to trigger redeployment:
   ```bash
   git add knowledge/docs/*.json
   git commit -m "Add verified agriculture sources"
   git push
   ```

4. **App auto-deploys** and uses new knowledge!

---

## 🎯 Sharing Your Link

### Share with Users

Share the UI link directly:
```
🌾 Kisan AI Assistant - Pakistani Agriculture Helper
https://your-app.platform.com/static/ui.html

Ask questions in Roman Urdu, Urdu, or English!
مثال: "Meri wheat pe rust aa gaya hai"
```

### For Developers (API Access)

Share the API endpoint:
```
POST https://your-app.platform.com/ask
Content-Type: application/json

{
  "query": "Your agriculture question",
  "language": "auto"
}
```

---

## 🔧 Troubleshooting

### App won't start?

1. **Check logs** on your platform's dashboard
2. **Verify** `requirements.txt` installed correctly
3. **Check** environment variables are set

### Out of memory?

1. **Use** `requirements-minimal.txt` instead:
   ```bash
   # In render.yaml or build command
   pip install -r requirements-minimal.txt
   ```

2. **Reduce** gunicorn workers:
   ```bash
   gunicorn -w 1 -b 0.0.0.0:$PORT app:app
   ```

### Slow response times?

1. **Add** knowledge base files (smaller files = faster indexing)
2. **Use** free tier with more resources (Railway, Fly.io)
3. **Consider** paid tier for production use

---

## 💰 Cost Comparison

| Platform | Free Tier Limits | Best For |
|----------|------------------|----------|
| **Render** | 750 hrs/month, 512MB RAM | Best overall free tier |
| **Railway** | $5 credit/month (~100 hrs) | Quick deploys, good DX |
| **Fly.io** | 3 VMs (256MB each) | Global edge deployment |
| **Cloud Run** | 2M requests, 360k GB-s | High traffic, pay-per-use |
| **Vercel** | Unlimited (serverless) | Serverless functions only |

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Fly.io Docs:** https://fly.io/docs
- **Cloud Run Docs:** https://cloud.google.com/run/docs

---

## ✅ Ready to Deploy!

1. **Choose a platform** (Render recommended)
2. **Follow the steps** above
3. **Get your link** in 5 minutes
4. **Share** with farmers and users! 🌾

**Your app will be live at:** `https://your-app.platform.com` ✨

---

**Need help?** Open an issue on GitHub or check platform documentation.

**اللہ حافظ | Good luck!** 🚀
