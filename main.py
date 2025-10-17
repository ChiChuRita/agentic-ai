import json
import random
import uuid
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from evaluator import MathEvaluator
from a2a_handler import (
    A2AAgentCard,
    parse_a2a_request,
    create_a2a_response,
    extract_skill_from_messages
)
import uvicorn

app = FastAPI(title="Math Evaluator Green Agent")
agent_app = FastAPI(title="Agent Server")
launcher_app = FastAPI(title="Launcher Server")

evaluator = MathEvaluator()

with open("math_problems.json", "r") as f:
    problems_data = json.load(f)
    PROBLEMS = {p["id"]: p for p in problems_data["problems"]}

session_problems: Dict[str, list] = {}


class ProblemRequest(BaseModel):
    session_id: str
    

class SolutionSubmission(BaseModel):
    session_id: str
    problem_id: str
    solution: str
    

class EvaluationResponse(BaseModel):
    score: int
    correct: bool
    feedback: str
    expected_answer: Optional[str] = None


@agent_app.get("/")
async def agent_root():
    return {
        "agent": "Math Evaluator Green Agent",
        "version": "1.0.0",
        "status": "running",
        "type": "evaluator",
        "description": "Provides math problems and evaluates solutions using GPT-5"
    }


@agent_app.get("/health")
async def agent_health():
    return {"status": "healthy", "service": "agent"}


@agent_app.get("/.well-known/agent.json")
async def agent_card():
    return A2AAgentCard.get_agent_card()


@agent_app.post("/a2a")
async def a2a_agent_endpoint(request: Request):
    try:
        data = await request.json()
        a2a_request = parse_a2a_request(data)
        
        task_id = a2a_request.task_id or str(uuid.uuid4())
        
        skill_id = a2a_request.skill_id
        parameters = a2a_request.parameters or {}
        
        if not skill_id and a2a_request.messages:
            skill_id, extracted_params = extract_skill_from_messages(a2a_request.messages)
            parameters.update(extracted_params)
        
        if skill_id == "get_math_problem":
            session_id = parameters.get("session_id", str(uuid.uuid4()))
            
            if session_id not in session_problems:
                session_problems[session_id] = []
            
            available_problems = [
                p for p_id, p in PROBLEMS.items() 
                if p_id not in session_problems[session_id]
            ]
            
            if not available_problems:
                return create_a2a_response(
                    task_id=task_id,
                    status="completed",
                    result={
                        "message": "All problems have been attempted",
                        "total_problems": len(PROBLEMS)
                    }
                )
            
            problem = random.choice(available_problems)
            session_problems[session_id].append(problem["id"])
            
            return create_a2a_response(
                task_id=task_id,
                status="completed",
                result={
                    "session_id": session_id,
                    "problem_id": problem["id"],
                    "problem": problem["problem"],
                    "difficulty": problem["difficulty"]
                }
            )
        
        elif skill_id == "evaluate_solution":
            session_id = parameters.get("session_id")
            problem_id = parameters.get("problem_id")
            solution = parameters.get("solution")
            
            if not all([session_id, problem_id, solution]):
                return create_a2a_response(
                    task_id=task_id,
                    status="failed",
                    error="Missing required parameters: session_id, problem_id, solution"
                )
            
            if problem_id not in PROBLEMS:
                return create_a2a_response(
                    task_id=task_id,
                    status="failed",
                    error=f"Problem {problem_id} not found"
                )
            
            problem = PROBLEMS[problem_id]
            
            evaluation = evaluator.evaluate_solution(
                problem=problem["problem"],
                expected_answer=problem["answer"],
                agent_solution=solution,
                explanation=problem.get("explanation", "")
            )
            
            return create_a2a_response(
                task_id=task_id,
                status="completed",
                result={
                    "session_id": session_id,
                    "problem_id": problem_id,
                    "score": evaluation["score"],
                    "correct": evaluation["correct"],
                    "feedback": evaluation["feedback"],
                    "expected_answer": problem["answer"] if evaluation["score"] < 100 else None
                }
            )
        
        else:
            return create_a2a_response(
                task_id=task_id,
                status="failed",
                error=f"Unknown skill: {skill_id}"
            )
    
    except Exception as e:
        return create_a2a_response(
            task_id=task_id if 'task_id' in locals() else str(uuid.uuid4()),
            status="failed",
            error=f"Error processing request: {str(e)}"
        )


@agent_app.post("/get_problem")
async def get_problem(request: ProblemRequest):
    session_id = request.session_id
    
    if session_id not in session_problems:
        session_problems[session_id] = []
    
    available_problems = [
        p for p_id, p in PROBLEMS.items() 
        if p_id not in session_problems[session_id]
    ]
    
    if not available_problems:
        return JSONResponse({
            "status": "completed",
            "message": "All problems have been attempted",
            "total_problems": len(PROBLEMS)
        })
    
    problem = random.choice(available_problems)
    session_problems[session_id].append(problem["id"])
    
    return {
        "problem_id": problem["id"],
        "problem": problem["problem"],
        "difficulty": problem["difficulty"]
    }


@agent_app.post("/submit_solution")
async def submit_solution(submission: SolutionSubmission):
    problem_id = submission.problem_id
    
    if problem_id not in PROBLEMS:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    problem = PROBLEMS[problem_id]
    
    evaluation = evaluator.evaluate_solution(
        problem=problem["problem"],
        expected_answer=problem["answer"],
        agent_solution=submission.solution,
        explanation=problem.get("explanation", "")
    )
    
    return EvaluationResponse(
        score=evaluation["score"],
        correct=evaluation["correct"],
        feedback=evaluation["feedback"],
        expected_answer=problem["answer"] if evaluation["score"] < 100 else None
    )


@agent_app.get("/problems")
async def list_problems():
    return {
        "total": len(PROBLEMS),
        "problems": [
            {
                "id": p["id"],
                "difficulty": p["difficulty"],
                "problem": p["problem"]
            }
            for p in PROBLEMS.values()
        ]
    }


@launcher_app.get("/")
async def launcher_root():
    agent_url = os.getenv("AGENT_URL", "http://localhost:8000")
    return {
        "launcher": "Math Evaluator Launcher",
        "version": "1.0.0",
        "status": "running",
        "agent_url": agent_url
    }


@launcher_app.get("/health")
async def launcher_health():
    return {"status": "healthy", "service": "launcher"}


@launcher_app.get("/.well-known/agent.json")
async def launcher_card():
    return A2AAgentCard.get_launcher_card()


@launcher_app.post("/a2a")
async def a2a_launcher_endpoint(request: Request):
    try:
        data = await request.json()
        a2a_request = parse_a2a_request(data)
        
        task_id = a2a_request.task_id or str(uuid.uuid4())
        
        skill_id = a2a_request.skill_id
        parameters = a2a_request.parameters or {}
        
        if not skill_id and a2a_request.messages:
            skill_id, extracted_params = extract_skill_from_messages(a2a_request.messages)
            parameters.update(extracted_params)
        
        if skill_id == "start_session":
            session_id = str(uuid.uuid4())
            session_problems[session_id] = []
            agent_url = os.getenv("AGENT_URL", "http://localhost:8000")
            
            return create_a2a_response(
                task_id=task_id,
                status="completed",
                result={
                    "session_id": session_id,
                    "total_problems": len(PROBLEMS),
                    "agent_url": agent_url
                }
            )
        
        elif skill_id == "get_session_status":
            session_id = parameters.get("session_id")
            
            if not session_id:
                return create_a2a_response(
                    task_id=task_id,
                    status="failed",
                    error="Missing required parameter: session_id"
                )
            
            if session_id not in session_problems:
                return create_a2a_response(
                    task_id=task_id,
                    status="failed",
                    error=f"Session {session_id} not found"
                )
            
            return create_a2a_response(
                task_id=task_id,
                status="completed",
                result={
                    "session_id": session_id,
                    "problems_attempted": len(session_problems[session_id]),
                    "total_problems": len(PROBLEMS),
                    "remaining": len(PROBLEMS) - len(session_problems[session_id])
                }
            )
        
        else:
            return create_a2a_response(
                task_id=task_id,
                status="failed",
                error=f"Unknown skill: {skill_id}"
            )
    
    except Exception as e:
        return create_a2a_response(
            task_id=task_id if 'task_id' in locals() else str(uuid.uuid4()),
            status="failed",
            error=f"Error processing request: {str(e)}"
        )


@launcher_app.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4())
    session_problems[session_id] = []
    agent_url = os.getenv("AGENT_URL", "http://localhost:8000")
    
    return {
        "session_id": session_id,
        "total_problems": len(PROBLEMS),
        "agent_url": agent_url
    }


@launcher_app.get("/session/{session_id}")
async def get_session_status(session_id: str):
    if session_id not in session_problems:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "problems_attempted": len(session_problems[session_id]),
        "total_problems": len(PROBLEMS),
        "remaining": len(PROBLEMS) - len(session_problems[session_id])
    }


def run_agent_server():
    uvicorn.run(agent_app, host="0.0.0.0", port=8000)


def run_launcher_server():
    uvicorn.run(launcher_app, host="0.0.0.0", port=8001)


def main():
    print("Math Evaluator Green Agent (A2A Protocol Compliant)")
    print("=" * 60)
    print("\nTo run the agent, use one of these commands:")
    print("  Agent Server:    uvicorn main:agent_app --host 0.0.0.0 --port 8000")
    print("  Launcher Server: uvicorn main:launcher_app --host 0.0.0.0 --port 8001")
    print("\nOr run both in separate terminals.")
    print("\n" + "=" * 60)
    print("REST API Endpoints:")
    print("  Agent:    http://localhost:8000")
    print("  Launcher: http://localhost:8001")
    print("\nA2A Protocol Endpoints:")
    print("  Agent Card:    http://localhost:8000/.well-known/agent.json")
    print("  Agent A2A:     http://localhost:8000/a2a")
    print("  Launcher Card: http://localhost:8001/.well-known/agent.json")
    print("  Launcher A2A:  http://localhost:8001/a2a")
    print("\n" + "=" * 60)
    print("Register on AgentBeats: https://agentbeats.org/login")


if __name__ == "__main__":
    main()
