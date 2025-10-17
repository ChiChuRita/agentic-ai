# Deploy to Render via CLI

## 🚀 Quick Deploy (Using render.yaml)

With the Render CLI, you can deploy directly from your terminal!

### Step 1: Login to Render

```bash
render login
```

This will open your browser to authenticate. Follow the prompts.

### Step 2: Commit Your Code

```bash
git add .
git commit -m "Ready for Render deployment"
```

### Step 3: Push to GitHub

```bash
# Create a repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 4: Deploy with Render CLI

```bash
render blueprint launch
```

This command will:

- Read your `render.yaml` file
- Create both services (agent + launcher)
- Deploy them automatically

### Step 5: Set Environment Variables

After deployment, set your environment variables:

```bash
# Set for agent service
render env set OPENAI_API_KEY=sk-proj-YOUR_KEY --service math-evaluator-agent
render env set AGENT_URL=https://math-evaluator-agent.onrender.com --service math-evaluator-agent

# Set for launcher service
render env set OPENAI_API_KEY=sk-proj-YOUR_KEY --service math-evaluator-launcher
render env set LAUNCHER_URL=https://math-evaluator-launcher.onrender.com --service math-evaluator-launcher
render env set AGENT_URL=https://math-evaluator-agent.onrender.com --service math-evaluator-launcher
```

**Note**: Replace the URLs with your actual service URLs after deployment.

### Step 6: View Your Services

```bash
# List all services
render services list

# View logs
render logs --service math-evaluator-agent
render logs --service math-evaluator-launcher
```

---

## 📋 Alternative: One-Command Deploy Script

I've created a `deploy.sh` script that automates everything:

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:

1. Check if you're logged into Render
2. Commit and push your code
3. Deploy using the blueprint
4. Guide you through setting environment variables

---

## 🔧 Useful Render CLI Commands

```bash
# Login
render login

# Deploy blueprint
render blueprint launch

# List services
render services list

# View service details
render service get math-evaluator-agent

# Set environment variable
render env set KEY=value --service SERVICE_NAME

# View logs (live tail)
render logs --service math-evaluator-agent --tail

# Restart service
render service restart math-evaluator-agent

# Delete service
render service delete math-evaluator-agent
```

---

## 🎯 Complete Example

```bash
# 1. Login
render login

# 2. Commit code
git add .
git commit -m "Deploy to Render"
git push

# 3. Deploy blueprint
render blueprint launch

# 4. Wait for deployment (check status)
render services list

# 5. Set environment variables (after getting actual URLs)
render env set OPENAI_API_KEY=sk-proj-xxx --service math-evaluator-agent
render env set AGENT_URL=https://math-evaluator-agent-abc123.onrender.com --service math-evaluator-agent

render env set OPENAI_API_KEY=sk-proj-xxx --service math-evaluator-launcher
render env set LAUNCHER_URL=https://math-evaluator-launcher-xyz789.onrender.com --service math-evaluator-launcher
render env set AGENT_URL=https://math-evaluator-agent-abc123.onrender.com --service math-evaluator-launcher

# 6. View logs to confirm
render logs --service math-evaluator-agent --tail
```

---

## ✅ Benefits of CLI Deployment

- ✅ **Faster**: No need to click through UI
- ✅ **Scriptable**: Can be automated
- ✅ **Version Control**: All config in `render.yaml`
- ✅ **Repeatable**: Easy to redeploy or deploy to different accounts
- ✅ **CI/CD Ready**: Can integrate with GitHub Actions

---

## 🆘 Troubleshooting

**Issue**: `render: command not found`

- **Solution**: Install with `brew install render`

**Issue**: `render login` fails

- **Solution**: Make sure you have a Render account at https://render.com

**Issue**: `render blueprint launch` fails

- **Solution**: Make sure your code is pushed to GitHub first

**Issue**: Can't find service name

- **Solution**: Run `render services list` to see exact service names

**Issue**: Environment variables not updating

- **Solution**: Services auto-redeploy when env vars change, wait 1-2 minutes

---

## 📚 Documentation

- Render CLI Docs: https://render.com/docs/cli
- Blueprint Docs: https://render.com/docs/infrastructure-as-code
