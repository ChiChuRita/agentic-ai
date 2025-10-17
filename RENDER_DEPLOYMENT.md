# Render Deployment Guide

## Prerequisites

1. Create a free account at [Render.com](https://render.com)
2. Install Git if not already installed
3. Have your OpenAI API key ready

## Step 1: Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
```

## Step 2: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

### Option A: Using render.yaml (Blueprint - Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and create both services

### Option B: Manual Deployment

#### Deploy Agent Service:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `math-evaluator-agent`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:agent_app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

#### Deploy Launcher Service:

1. Repeat the above steps with:
   - **Name**: `math-evaluator-launcher`
   - **Start Command**: `uvicorn main:launcher_app --host 0.0.0.0 --port $PORT`

## Step 4: Configure Environment Variables

For each service, add these environment variables in the Render dashboard:

### Agent Service:

- `OPENAI_API_KEY`: Your OpenAI API key
- `AGENT_URL`: `https://YOUR-AGENT-SERVICE.onrender.com` (you'll get this after deployment)

### Launcher Service:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LAUNCHER_URL`: `https://YOUR-LAUNCHER-SERVICE.onrender.com` (you'll get this after deployment)
- `AGENT_URL`: `https://YOUR-AGENT-SERVICE.onrender.com`

## Step 5: Get Your Public URLs

After deployment, you'll receive URLs like:

- Agent: `https://math-evaluator-agent.onrender.com`
- Launcher: `https://math-evaluator-launcher.onrender.com`

## Step 6: Update Environment Variables

Go back to each service and update the `AGENT_URL` and `LAUNCHER_URL` with the actual deployed URLs.

## Step 7: Test Your Deployment

```bash
# Test agent health
curl https://YOUR-AGENT-URL.onrender.com/health

# Test launcher health
curl https://YOUR-LAUNCHER-URL.onrender.com/health

# Test agent card
curl https://YOUR-AGENT-URL.onrender.com/.well-known/agent.json

# Test launcher card
curl https://YOUR-LAUNCHER-URL.onrender.com/.well-known/agent.json
```

## Step 8: Register on AgentBeats

1. Go to [AgentBeats](https://agentbeats.org/login)
2. Register your agent using the public URLs

## Notes

- Free tier on Render spins down after 15 minutes of inactivity
- First request after spin-down will take ~30 seconds
- For production, consider upgrading to a paid plan
- Make sure to add your OpenAI API key as an environment variable
- Never commit `.env` file with secrets to GitHub

## Troubleshooting

If deployment fails:

1. Check the logs in Render dashboard
2. Ensure `requirements.txt` is present
3. Verify Python version compatibility
4. Check that all environment variables are set correctly
