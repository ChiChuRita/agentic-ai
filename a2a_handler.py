from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid
import os
from datetime import datetime


class A2AMessage(BaseModel):
    role: str
    content: str


class A2ATaskRequest(BaseModel):
    task_id: Optional[str] = None
    messages: List[A2AMessage]
    skill_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class A2ATaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


class A2AAgentCard:
    @staticmethod
    def get_agent_card() -> Dict[str, Any]:
        agent_url = os.getenv("AGENT_URL", "http://localhost:8000")
        return {
            "schema_version": "1.0.0",
            "name": "Math Evaluator Green Agent",
            "description": "Evaluates math problem solutions using GPT-5. Provides custom math problems and grades agent responses.",
            "versions": [
                {
                    "version": "1.0.0",
                    "endpoint": f"{agent_url}/a2a",
                    "supports_streaming": False,
                    "auth": {
                        "type": "none"
                    }
                }
            ],
            "capabilities": {
                "skills": [
                    {
                        "id": "get_math_problem",
                        "name": "Get Math Problem",
                        "description": "Provides a random math problem from the curated problem set",
                        "parameters": {
                            "session_id": {
                                "type": "string",
                                "required": True,
                                "description": "Session identifier to track problem distribution"
                            }
                        }
                    },
                    {
                        "id": "evaluate_solution",
                        "name": "Evaluate Math Solution",
                        "description": "Evaluates a submitted math solution using GPT-5",
                        "parameters": {
                            "session_id": {
                                "type": "string",
                                "required": True
                            },
                            "problem_id": {
                                "type": "string",
                                "required": True
                            },
                            "solution": {
                                "type": "string",
                                "required": True
                            }
                        }
                    }
                ]
            },
            "contact_email": "ra.singh069@gmail.com"
        }
    
    @staticmethod
    def get_launcher_card() -> Dict[str, Any]:
        launcher_url = os.getenv("LAUNCHER_URL", "http://localhost:8001")
        return {
            "schema_version": "1.0.0",
            "name": "Math Evaluator Launcher",
            "description": "Manages evaluation sessions and coordinates between agents",
            "versions": [
                {
                    "version": "1.0.0",
                    "endpoint": f"{launcher_url}/a2a",
                    "supports_streaming": False,
                    "auth": {
                        "type": "none"
                    }
                }
            ],
            "capabilities": {
                "skills": [
                    {
                        "id": "start_session",
                        "name": "Start Evaluation Session",
                        "description": "Creates a new evaluation session",
                        "parameters": {}
                    },
                    {
                        "id": "get_session_status",
                        "name": "Get Session Status",
                        "description": "Retrieves current session status",
                        "parameters": {
                            "session_id": {
                                "type": "string",
                                "required": True
                            }
                        }
                    }
                ]
            },
            "contact_email": "support@agenticai.example.com"
        }


def parse_a2a_request(data: Dict[str, Any]) -> A2ATaskRequest:
    return A2ATaskRequest(**data)


def create_a2a_response(
    task_id: str,
    status: str = "completed",
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    if not task_id:
        task_id = str(uuid.uuid4())
    
    response = A2ATaskResponse(
        task_id=task_id,
        status=status,
        result=result,
        error=error,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
    
    return response.model_dump(exclude_none=True)


def extract_skill_from_messages(messages: List[A2AMessage]) -> tuple[Optional[str], Dict[str, Any]]:
    if not messages:
        return None, {}
    
    last_message = messages[-1]
    content = last_message.content
    
    parameters = {}
    skill_id = None
    
    if "get problem" in content.lower() or "math problem" in content.lower():
        skill_id = "get_math_problem"
        if "session" in content.lower():
            import re
            session_match = re.search(r'session[_\s]+(?:id[:\s]+)?([a-zA-Z0-9-]+)', content, re.IGNORECASE)
            if session_match:
                parameters["session_id"] = session_match.group(1)
    
    elif "evaluate" in content.lower() or "grade" in content.lower() or "check" in content.lower():
        skill_id = "evaluate_solution"
        import re
        session_match = re.search(r'session[_\s]+(?:id[:\s]+)?([a-zA-Z0-9-]+)', content, re.IGNORECASE)
        problem_match = re.search(r'problem[_\s]+(?:id[:\s]+)?([0-9]+)', content, re.IGNORECASE)
        solution_match = re.search(r'(?:solution|answer)[:\s]+([^\n]+)', content, re.IGNORECASE)
        
        if session_match:
            parameters["session_id"] = session_match.group(1)
        if problem_match:
            parameters["problem_id"] = problem_match.group(1)
        if solution_match:
            parameters["solution"] = solution_match.group(1).strip()
    
    elif "start session" in content.lower() or "new session" in content.lower():
        skill_id = "start_session"
    
    elif "session status" in content.lower() or "check session" in content.lower():
        skill_id = "get_session_status"
        import re
        session_match = re.search(r'session[_\s]+(?:id[:\s]+)?([a-zA-Z0-9-]+)', content, re.IGNORECASE)
        if session_match:
            parameters["session_id"] = session_match.group(1)
    
    return skill_id, parameters

