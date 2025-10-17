# Render UI Configuration Guide

## 📋 What to Enter in Render Dashboard

> **Note**: We're using `uv` for faster dependency installation. The build command installs `uv` first, then uses it to install your dependencies. This is faster than using `pip` alone.
>
> If you prefer standard `pip`, change the build command to: `pip install -r requirements.txt`

### Option 1: Blueprint Deployment (Easiest - Recommended)

1. **Go to**: https://dashboard.render.com/
2. **Click**: "New" button (top right) → Select "Blueprint"
3. **Connect GitHub**: If first time, authorize Render to access your GitHub
4. **Select Repository**: Choose your `agentic-ai` repository
5. **Click**: "Apply"

Render will automatically create both services from `render.yaml`. After services are created, proceed to add environment variables below.

---

### Option 2: Manual Deployment (If Blueprint doesn't work)

#### Service 1: Agent Service

**Step 1 - Click**: "New" → "Web Service"

**Step 2 - Connect Repository**: Select your GitHub repository

**Step 3 - Configure Service**:

| Field             | Value                                                           |
| ----------------- | --------------------------------------------------------------- |
| **Name**          | `math-evaluator-agent`                                          |
| **Region**        | Choose closest to you (e.g., Oregon, Ohio, Frankfurt)           |
| **Branch**        | `main`                                                          |
| **Runtime**       | `Python 3`                                                      |
| **Build Command** | `pip install uv && uv pip install --system -r requirements.txt` |
| **Start Command** | `uvicorn main:agent_app --host 0.0.0.0 --port $PORT`            |
| **Instance Type** | `Free`                                                          |

**Step 4 - Advanced Settings** (Optional):

- **Health Check Path**: `/health`
- **Auto-Deploy**: Yes (recommended)

**Click**: "Create Web Service"

---

#### Service 2: Launcher Service

**Step 1 - Click**: "New" → "Web Service"

**Step 2 - Connect Repository**: Select your GitHub repository (same as above)

**Step 3 - Configure Service**:

| Field             | Value                                                           |
| ----------------- | --------------------------------------------------------------- |
| **Name**          | `math-evaluator-launcher`                                       |
| **Region**        | Same as agent service                                           |
| **Branch**        | `main`                                                          |
| **Runtime**       | `Python 3`                                                      |
| **Build Command** | `pip install uv && uv pip install --system -r requirements.txt` |
| **Start Command** | `uvicorn main:launcher_app --host 0.0.0.0 --port $PORT`         |
| **Instance Type** | `Free`                                                          |

**Step 4 - Advanced Settings** (Optional):

- **Health Check Path**: `/health`
- **Auto-Deploy**: Yes (recommended)

**Click**: "Create Web Service"

---

## 🔑 Environment Variables to Add

### For `math-evaluator-agent` Service:

**Where**: Go to service → "Environment" tab → "Add Environment Variable"

| Key              | Value                                       | Notes                                |
| ---------------- | ------------------------------------------- | ------------------------------------ |
| `OPENAI_API_KEY` | `sk-proj-...`                               | Your actual OpenAI API key           |
| `AGENT_URL`      | `https://math-evaluator-agent.onrender.com` | Will be available after first deploy |

**Steps**:

1. Click on `math-evaluator-agent` service
2. Click "Environment" in left sidebar
3. Click "Add Environment Variable"
4. Enter key: `OPENAI_API_KEY`
5. Enter value: Your OpenAI API key
6. Click "Save Changes"
7. Repeat for `AGENT_URL` (after you get the actual URL from Render)

---

### For `math-evaluator-launcher` Service:

**Where**: Go to service → "Environment" tab → "Add Environment Variable"

| Key              | Value                                          | Notes                                |
| ---------------- | ---------------------------------------------- | ------------------------------------ |
| `OPENAI_API_KEY` | `sk-proj-...`                                  | Your actual OpenAI API key           |
| `LAUNCHER_URL`   | `https://math-evaluator-launcher.onrender.com` | Will be available after first deploy |
| `AGENT_URL`      | `https://math-evaluator-agent.onrender.com`    | Copy from agent service URL          |

**Steps**:

1. Click on `math-evaluator-launcher` service
2. Click "Environment" in left sidebar
3. Click "Add Environment Variable"
4. Enter key: `OPENAI_API_KEY`
5. Enter value: Your OpenAI API key
6. Click "Save Changes"
7. Repeat for `LAUNCHER_URL` and `AGENT_URL`

---

## 📝 Two-Step Process for URLs

### Step 1: Initial Deployment

1. Deploy both services **without** the URL environment variables
2. Let them deploy (they'll use localhost URLs initially)
3. Copy the URLs Render gives you (e.g., `https://math-evaluator-agent-xyz.onrender.com`)

### Step 2: Add URL Variables

1. Go to each service
2. Add the environment variables with the **actual URLs** from Step 1
3. Render will automatically redeploy with the correct URLs

---

## 🔍 Where to Find Your URLs

After deployment, each service page shows:

```
Your service is live at:
https://math-evaluator-agent-xxxx.onrender.com
```

Copy these URLs and use them in the environment variables.

---

## ✅ Verification

After adding environment variables, test:

```bash
# Replace with your actual URLs
curl https://your-agent-url.onrender.com/health
curl https://your-launcher-url.onrender.com/health
curl https://your-agent-url.onrender.com/.well-known/agent.json
```

Expected responses:

- Health checks: `{"status":"healthy","service":"agent"}` or `"launcher"`
- Agent card: JSON with agent configuration

---

## 🎯 Quick Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Blueprint or both services on Render
- [ ] Services deployed successfully (green status)
- [ ] Added `OPENAI_API_KEY` to both services
- [ ] Copied actual URLs from Render dashboard
- [ ] Added `AGENT_URL` to agent service
- [ ] Added `AGENT_URL` and `LAUNCHER_URL` to launcher service
- [ ] Services redeployed automatically
- [ ] Tested all health endpoints
- [ ] Tested agent card endpoints
- [ ] Ready to register on AgentBeats!

---

## 💡 Pro Tips

1. **URLs format**: They'll be like `https://SERVICE-NAME-abcd1234.onrender.com`
2. **No trailing slash**: Don't add `/` at the end of URLs
3. **HTTPS only**: Render only provides HTTPS URLs
4. **Free tier sleeps**: Services sleep after 15 min inactivity (30s wake up time)
5. **Logs**: Check "Logs" tab if something fails

---

## 🆘 Common Issues

**Issue**: Service fails to start

- **Solution**: Check "Logs" tab, ensure `requirements.txt` is correct

**Issue**: Health check failing

- **Solution**: Ensure path is `/health` and service is listening on `$PORT`

**Issue**: Can't find environment variables

- **Solution**: Click service name → "Environment" in left sidebar

**Issue**: Changes not reflecting

- **Solution**: Render auto-deploys on variable changes, wait 1-2 minutes
