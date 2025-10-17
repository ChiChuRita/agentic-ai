# Running the Green Agent Evaluator

## Setup Overview

Your green agent is an **evaluator** that white agents test against. Here's how to set it up:

## Step 1: Prerequisites

Make sure you have:

1. Installed dependencies: `uv sync`
2. Created `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_actual_api_key" > .env
   ```

## Step 2: Start the Green Agent

Run your green agent servers:

```bash
python run_agent.py
```

This starts:

- **Agent Server** on `http://localhost:8000` (provides problems, evaluates solutions)
- **Launcher Server** on `http://localhost:8001` (manages sessions)

You should see:

```
Starting Math Evaluator Green Agent...
============================================================

Agent Server:    http://localhost:8000
Launcher Server: http://localhost:8001

Press Ctrl+C to stop both servers
============================================================
```

## Step 3: Test Your Green Agent (Optional)

In a separate terminal, run the test suite:

```bash
python test_agent.py
```

This will test:

- REST API endpoints
- A2A protocol endpoints
- Agent card discovery
- Problem distribution
- GPT-5 evaluation

## Step 4: Make Agent Accessible to AgentBeats

### For Local Testing (Same Machine)

Your agent is already accessible at:

- Agent: `http://localhost:8000`
- Launcher: `http://localhost:8001`

White agents on your machine can connect directly to these URLs.

### For Remote Access (AgentBeats Platform)

If white agents need to access your green agent remotely, expose it via ngrok:

**Terminal 3 - Expose Agent Server:**

```bash
ngrok http 8000
```

**Terminal 4 - Expose Launcher Server:**

```bash
ngrok http 8001
```

Note the ngrok URLs (e.g., `https://abc123.ngrok.io`).

## Step 5: Register on AgentBeats (Optional)

If you want to list your agent on the AgentBeats platform:

1. Visit https://agentbeats.org/login
2. Register your agent with:
   - **Agent URL:** `http://localhost:8000` (or your ngrok URL)
   - **Launcher URL:** `http://localhost:8001` (or your ngrok URL)
   - **Description:** "Math problem evaluator - provides 15 custom math problems and grades solutions using GPT-5"

## How White Agents Connect

White agents can now test against your green agent:

### Discovery (A2A Protocol)

```bash
# White agent fetches your agent card
curl http://localhost:8000/.well-known/agent.json
```

### Request Problem

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "get_math_problem",
    "parameters": {"session_id": "test-123"}
  }'
```

### Submit Solution for Evaluation

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "evaluate_solution",
    "parameters": {
      "session_id": "test-123",
      "problem_id": "1",
      "solution": "42"
    }
  }'
```

## Running White Agents to Test Your Green Agent

If you want to run a white agent (e.g., from the red_agent_card.toml example) to test against your green agent:

```bash
# In another project directory with a white/red agent
agentbeats run white_agent_card.toml \
  --agent_host localhost \
  --agent_port <white_agent_port> \
  --launcher_host localhost \
  --launcher_port <white_launcher_port> \
  --model_type openai \
  --model_name gpt-4

# The white agent will then connect to your green agent at:
# http://localhost:8000 and http://localhost:8001
```

## Architecture

```
┌─────────────────────────────────────┐
│   White Agents (Testing Agents)    │
│  - Solve math problems              │
│  - Submit solutions                 │
└──────────────┬──────────────────────┘
               │
               │ A2A Protocol
               │ (Discover, Request, Submit)
               │
               ▼
┌─────────────────────────────────────┐
│   Green Agent (Your Evaluator)      │
│                                     │
│  Agent Server :8000                 │
│  - Provides math problems           │
│  - Evaluates solutions (GPT-5)      │
│  - Returns scores & feedback        │
│                                     │
│  Launcher Server :8001              │
│  - Manages sessions                 │
│  - Tracks progress                  │
└─────────────────────────────────────┘
```

## Stopping the Green Agent

Press `Ctrl+C` in the terminal where `run_agent.py` is running.

## Troubleshooting

**Port already in use:**

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

**OpenAI API key error:**

- Make sure `.env` file exists in the project root
- Verify the API key is correct
- Check you have GPT-5 access

**White agents can't connect:**

- Verify green agent is running: `curl http://localhost:8000/health`
- Check firewall settings
- Use ngrok for remote access
