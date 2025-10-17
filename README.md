# Green Agent Math Evaluator for AgentBeats

A green agent evaluator that provides math problems and grades solutions from white agents on the [AgentBeats](https://agentbeats.org/) platform using OpenAI GPT-5.

**✅ Fully A2A Protocol Compliant** - Implements the [Agent-to-Agent (A2A) protocol](https://www.a2aprotocol.net/) for standardized agent communication.

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Set up your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run the green agent (evaluator)
python run_agent.py

# Your green agent is now running on:
# - Agent Server: http://localhost:8000
# - Launcher Server: http://localhost:8001

# 4. Test it (in another terminal)
python test_agent.py

# 5. White agents can now connect to your green agent!
#    They'll discover your capabilities via the agent card at:
#    http://localhost:8000/.well-known/agent.json
```

**📖 For detailed setup instructions, see [RUNNING_GUIDE.md](RUNNING_GUIDE.md)**

## Overview

This agent:

- Hosts 15 custom math problems (easy, medium, and hard difficulty)
- Provides problems to white agents via API endpoints
- Evaluates solutions using GPT-5 for intelligent grading
- Supports partial credit and alternative solution methods
- Tracks sessions and problem attempts

## Prerequisites

- Python 3.13+
- OpenAI API key with GPT-5 access
- UV package manager (or pip)

## Installation

1. **Clone or navigate to the project:**

   ```bash
   cd /Users/chichurita/Dev/agentic-ai
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -e .
   ```

3. **Set up your OpenAI API key:**

   Create a `.env` file in the project root:

   ```bash
   echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
   ```

   Replace `your_actual_api_key_here` with your OpenAI API key.

## Running the Agent

The agent consists of two servers that need to run simultaneously:

### Option 1: Run both servers with the helper script (Recommended)

```bash
python run_agent.py
```

This starts both the agent and launcher servers in a single process.

### Option 2: Run in separate terminals

**Terminal 1 - Agent Server:**

```bash
uvicorn main:agent_app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Launcher Server:**

```bash
uvicorn main:launcher_app --host 0.0.0.0 --port 8001
```

### Option 3: View instructions

```bash
python main.py
```

This displays the URLs and instructions without starting servers.

## API Endpoints

### Agent Server (Port 8000)

#### REST API Endpoints

- `GET /` - Agent information
- `GET /health` - Health check
- `POST /get_problem` - Get a random math problem
  ```json
  {
    "session_id": "your-session-id"
  }
  ```
- `POST /submit_solution` - Submit a solution for evaluation
  ```json
  {
    "session_id": "your-session-id",
    "problem_id": "1",
    "solution": "42"
  }
  ```
- `GET /problems` - List all available problems

#### A2A Protocol Endpoints

- `GET /.well-known/agent.json` - Agent card (capabilities, skills, metadata)
- `POST /a2a` - A2A protocol communication endpoint
  ```json
  {
    "task_id": "unique-task-id",
    "skill_id": "get_math_problem",
    "parameters": {
      "session_id": "session-123"
    },
    "messages": [
      {
        "role": "user",
        "content": "Get me a math problem"
      }
    ]
  }
  ```

### Launcher Server (Port 8001)

#### REST API Endpoints

- `GET /` - Launcher information
- `GET /health` - Health check
- `POST /start_session` - Create a new evaluation session
- `GET /session/{session_id}` - Get session status

#### A2A Protocol Endpoints

- `GET /.well-known/agent.json` - Launcher card (capabilities, skills, metadata)
- `POST /a2a` - A2A protocol communication endpoint

## Registering on AgentBeats

1. Start both servers (agent and launcher)

2. Visit [AgentBeats Login](https://agentbeats.org/login)

3. Register your agent with:

   - **Agent URL:** `http://localhost:8000`
   - **Launcher URL:** `http://localhost:8001`
   - **Description:** "Math problem evaluator agent - provides custom math problems and grades solutions using GPT-5"

4. For remote access (if AgentBeats requires public URLs):
   - Use ngrok or similar tunneling service:
     ```bash
     ngrok http 8000
     ngrok http 8001
     ```
   - Use the ngrok URLs instead of localhost

## Agent Card Configuration

The agent follows the standard AgentBeats agent card format (see `agent_card.toml` and `launcher_card.toml`):

- **Skills Defined:**
  - `get_math_problem` - Provides random math problems
  - `evaluate_solution` - Grades solutions using GPT-5
  - `session_management` - Tracks evaluation sessions
- **Capabilities:**
  - Text input/output modes
  - Non-streaming responses
  - A2A (Agent-to-Agent) protocol support

The agent card format is compatible with AgentBeats MCP/A2A protocols for standardized agent communication.

## A2A Protocol Integration

This agent fully implements the Agent-to-Agent (A2A) protocol for standardized communication:

### Agent Card Discovery

Both agent and launcher expose agent cards at the standard location:

```bash
curl http://localhost:8000/.well-known/agent.json
curl http://localhost:8001/.well-known/agent.json
```

The agent card provides:

- Agent metadata (name, description, version)
- Available skills and their parameters
- A2A endpoint URL
- Authentication requirements (none for this implementation)

### A2A Communication Format

The A2A endpoint accepts requests in this format:

```json
{
  "task_id": "unique-task-identifier",
  "skill_id": "skill_name",
  "parameters": {
    "param1": "value1"
  },
  "messages": [
    {
      "role": "user",
      "content": "Natural language description of the task"
    }
  ]
}
```

And returns responses in this format:

```json
{
  "task_id": "unique-task-identifier",
  "status": "completed",
  "result": {
    "key": "value"
  },
  "timestamp": "2024-10-17T12:00:00Z"
}
```

### Available Skills

**Agent Skills (Port 8000):**

- `get_math_problem` - Provides a random math problem
- `evaluate_solution` - Evaluates a submitted solution using GPT-5

**Launcher Skills (Port 8001):**

- `start_session` - Creates a new evaluation session
- `get_session_status` - Retrieves session progress

### Example A2A Requests

**Start a Session:**

```bash
curl -X POST http://localhost:8001/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task-001",
    "skill_id": "start_session",
    "messages": [{"role": "user", "content": "Start new session"}]
  }'
```

**Get a Problem:**

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task-002",
    "skill_id": "get_math_problem",
    "parameters": {"session_id": "your-session-id"},
    "messages": [{"role": "user", "content": "Get math problem"}]
  }'
```

**Evaluate a Solution:**

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task-003",
    "skill_id": "evaluate_solution",
    "parameters": {
      "session_id": "your-session-id",
      "problem_id": "1",
      "solution": "42"
    },
    "messages": [{"role": "user", "content": "Evaluate my solution"}]
  }'
```

## Testing Locally

### Automated Test Script (Recommended)

Run the test script to verify your agent is working:

```bash
python test_agent.py
```

This will:

1. Check both server health endpoints
2. Start a test session
3. Get a problem
4. Submit a solution
5. Get GPT-5 evaluation
6. Check session status
7. List all problems

### Manual Testing with curl

You can also test the agent manually using curl:

```bash
# Check agent health
curl http://localhost:8000/health

# Start a session
curl -X POST http://localhost:8001/start_session

# Get a problem (replace SESSION_ID)
curl -X POST http://localhost:8000/get_problem \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID"}'

# Submit a solution
curl -X POST http://localhost:8000/submit_solution \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "problem_id": "1",
    "solution": "42"
  }'
```

## Project Structure

```
agentic-ai/
├── main.py                 # FastAPI servers (agent & launcher) with A2A endpoints
├── evaluator.py           # GPT-5 evaluation logic
├── a2a_handler.py         # A2A protocol message parsing and formatting
├── math_problems.json     # Problem dataset (15 problems)
├── agent_card.toml        # Agent configuration (AgentBeats format)
├── launcher_card.toml     # Launcher configuration (AgentBeats format)
├── run_agent.py           # Helper script to run both servers
├── test_agent.py          # Automated test suite (REST + A2A)
├── pyproject.toml         # Python dependencies
├── .env                   # API keys (create this)
├── README.md              # This file
└── RUNNING_GUIDE.md       # Detailed setup and running instructions
```

## Math Problems

The agent includes 15 problems across three difficulty levels:

- **Easy:** Basic arithmetic and geometry (5 problems)
- **Medium:** Algebra, percentages, and word problems (6 problems)
- **Hard:** Complex algebra, multi-step problems (4 problems)

## Evaluation Logic

The GPT-5 evaluator:

- Compares agent solutions against expected answers
- Accepts equivalent forms (e.g., 0.5 vs 1/2)
- Provides partial credit for partially correct solutions
- Gives detailed feedback on incorrect answers
- Returns scores from 0-100

## Development

To modify the problems, edit `math_problems.json`:

```json
{
  "problems": [
    {
      "id": "16",
      "difficulty": "medium",
      "problem": "Your problem here",
      "answer": "Expected answer",
      "explanation": "Solution explanation"
    }
  ]
}
```

## Troubleshooting

**Issue:** `OPENAI_API_KEY not found`

- **Solution:** Create a `.env` file with your API key

**Issue:** Port already in use

- **Solution:** Change ports in `agent_card.toml` or use different ports when running

**Issue:** AgentBeats can't reach localhost

- **Solution:** Use ngrok or deploy to a public server

## License

MIT
