# Quick Deploy to Render

## ✅ What's Been Done

Your project is now ready for Render deployment with:

- ✅ `render.yaml` - Blueprint configuration for automatic deployment
- ✅ `requirements.txt` - Python dependencies
- ✅ Environment variable support for dynamic URLs
- ✅ Updated agent cards to use configurable endpoints
- ✅ Both services configured (agent on port 8000, launcher on port 8001)

## 🚀 Deploy Now - 5 Steps

### 1. Commit Your Code

```bash
git add .
git commit -m "Ready for Render deployment"
```

### 2. Push to GitHub

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 3. Deploy on Render

1. Go to https://dashboard.render.com/
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Select your repo
5. Click **Apply** - Render will create both services automatically!

### 4. Add Environment Variables

After deployment, for **EACH** service, add these environment variables:

#### For `math-evaluator-agent`:

```
OPENAI_API_KEY=your_actual_openai_api_key
AGENT_URL=https://math-evaluator-agent.onrender.com
```

#### For `math-evaluator-launcher`:

```
OPENAI_API_KEY=your_actual_openai_api_key
LAUNCHER_URL=https://math-evaluator-launcher.onrender.com
AGENT_URL=https://math-evaluator-agent.onrender.com
```

_(Note: Replace with your actual service URLs from Render)_

### 5. Test Your Deployment

After services are live, test them:

```bash
# Get your URLs from Render dashboard, then test:
curl https://math-evaluator-agent.onrender.com/health
curl https://math-evaluator-launcher.onrender.com/health
curl https://math-evaluator-agent.onrender.com/.well-known/agent.json
```

## 📋 Your Public Endpoints

Once deployed, you'll have:

### Agent Service

- Base URL: `https://math-evaluator-agent.onrender.com`
- Health: `https://math-evaluator-agent.onrender.com/health`
- Agent Card: `https://math-evaluator-agent.onrender.com/.well-known/agent.json`
- A2A Endpoint: `https://math-evaluator-agent.onrender.com/a2a`

### Launcher Service

- Base URL: `https://math-evaluator-launcher.onrender.com`
- Health: `https://math-evaluator-launcher.onrender.com/health`
- Launcher Card: `https://math-evaluator-launcher.onrender.com/.well-known/agent.json`
- A2A Endpoint: `https://math-evaluator-launcher.onrender.com/a2a`

## 🎯 Register on AgentBeats

Once deployed and tested:

1. Go to https://agentbeats.org/login
2. Register your agent using the A2A endpoints above
3. Share your agent card URLs

## ⚠️ Important Notes

- **Free Tier**: Services spin down after 15 minutes of inactivity
- **Cold Start**: First request after spin-down takes ~30 seconds
- **API Key**: Make sure your OpenAI API key is valid and has credits
- **URLs**: Update environment variables with actual Render URLs after deployment
- **Never commit `.env`** with secrets - it's already in `.gitignore`

## 🔧 Troubleshooting

If deployment fails:

1. Check logs in Render dashboard (click on service → Logs)
2. Verify `requirements.txt` exists
3. Make sure all environment variables are set
4. Ensure your OpenAI API key is valid

## 📝 Next Steps After Deployment

1. Test all endpoints are working
2. Update environment variables with actual URLs
3. Register on AgentBeats
4. Monitor logs for any errors
5. Test A2A protocol communication

---

**Need help?** Check the full guide in `RENDER_DEPLOYMENT.md`
