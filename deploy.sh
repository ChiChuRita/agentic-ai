#!/bin/bash

set -e

echo "🚀 Render Deployment Script"
echo "============================"
echo ""

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI is not installed"
    echo "Install it with: brew install render"
    exit 1
fi

# Check if logged in
echo "📝 Checking Render authentication..."
if ! render services list &> /dev/null; then
    echo "❌ Not logged into Render"
    echo "Please run: render login"
    exit 1
fi

echo "✅ Authenticated with Render"
echo ""

# Check if git is initialized
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "📦 Initializing git repository..."
    git init
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "⚠️  No GitHub remote found"
    echo "Please create a GitHub repository and run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo ""
    read -p "Have you added the remote? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Commit changes
echo "📦 Committing changes..."
git add .
if git diff-index --quiet HEAD --; then
    echo "✅ No changes to commit"
else
    git commit -m "Deploy to Render via CLI" || true
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main || git push

echo ""
echo "🚀 Deploying to Render using render.yaml..."
echo ""

# Deploy blueprint
render blueprint launch

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "⏳ Services are now being deployed. This may take 3-5 minutes."
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Wait for services to deploy (check status with: render services list)"
echo ""
echo "2. Get your service URLs from the Render dashboard or CLI"
echo ""
echo "3. Set environment variables (replace with your actual values):"
echo ""
echo "   # For agent service:"
echo "   render env set OPENAI_API_KEY=sk-proj-YOUR_KEY --service math-evaluator-agent"
echo "   render env set AGENT_URL=https://YOUR-AGENT-URL.onrender.com --service math-evaluator-agent"
echo ""
echo "   # For launcher service:"
echo "   render env set OPENAI_API_KEY=sk-proj-YOUR_KEY --service math-evaluator-launcher"
echo "   render env set LAUNCHER_URL=https://YOUR-LAUNCHER-URL.onrender.com --service math-evaluator-launcher"
echo "   render env set AGENT_URL=https://YOUR-AGENT-URL.onrender.com --service math-evaluator-launcher"
echo ""
echo "4. View logs:"
echo "   render logs --service math-evaluator-agent --tail"
echo ""
echo "5. Test your endpoints:"
echo "   curl https://YOUR-AGENT-URL.onrender.com/health"
echo ""
echo "🎉 Happy deploying!"

