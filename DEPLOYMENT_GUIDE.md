# 🚀 Streamlit Cloud Deployment Guide

## Step-by-Step Instructions

### 1. Go to Streamlit Cloud
Visit: **https://share.streamlit.io**

### 2. Sign In
- Click "Sign in" (top right corner)
- Choose "Continue with GitHub"
- Sign in with your GitHub account: **ekumarchitturu-cmd**

### 3. Create New App
- Click the "New app" button
- If asked, authorize Streamlit to access your GitHub repositories

### 4. Fill in the Deployment Form

**Repository settings:**
- Repository: `ekumarchitturu-cmd/studyforge`
- Branch: `main`
- Main file path: `app.py`

### 5. Add Secrets (IMPORTANT!)
- Click "Advanced settings" at the bottom
- In the "Secrets" text box, paste your OpenAI API key in this format:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

**Note:** Use the API key from your `.env` file

### 6. Deploy!
- Click "Deploy!" button
- Wait 2-3 minutes for deployment to complete

### 7. Your App is LIVE! 🎉
You'll get a URL like: `https://studyforge-xxxxx.streamlit.app`

Share this URL with anyone to use your app!

---

## Troubleshooting

**If deployment fails:**
1. Check that the secrets are pasted correctly (no extra spaces)
2. Make sure the OPENAI_API_KEY is correct
3. Check the logs in Streamlit Cloud dashboard

**If the app shows errors:**
1. Click on "Manage app" → "Logs" to see what's wrong
2. Most common issue: Missing or incorrect API key in secrets

---

## After Deployment

Your app will be available 24/7 on the internet!
- Free hosting
- Automatic HTTPS
- Updates when you push to GitHub

**To update the app later:**
Just push changes to GitHub and Streamlit will auto-redeploy!
