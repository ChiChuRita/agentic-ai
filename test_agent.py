import requests
import json
import time


def test_agent():
    print("Testing Math Evaluator Green Agent (A2A Protocol Compliant)")
    print("=" * 60)
    
    agent_url = "http://localhost:8000"
    launcher_url = "http://localhost:8001"
    
    print("\n1. Testing Agent Health...")
    try:
        response = requests.get(f"{agent_url}/health")
        print(f"   ✓ Agent: {response.json()}")
    except Exception as e:
        print(f"   ✗ Agent health check failed: {e}")
        print("   Make sure the agent server is running on port 8000")
        return
    
    print("\n2. Testing Launcher Health...")
    try:
        response = requests.get(f"{launcher_url}/health")
        print(f"   ✓ Launcher: {response.json()}")
    except Exception as e:
        print(f"   ✗ Launcher health check failed: {e}")
        print("   Make sure the launcher server is running on port 8001")
        return
    
    print("\n3. Starting a Session...")
    try:
        response = requests.post(f"{launcher_url}/start_session")
        session_data = response.json()
        session_id = session_data["session_id"]
        print(f"   ✓ Session ID: {session_id}")
        print(f"   Total problems available: {session_data['total_problems']}")
    except Exception as e:
        print(f"   ✗ Failed to start session: {e}")
        return
    
    print("\n4. Getting a Problem...")
    try:
        response = requests.post(
            f"{agent_url}/get_problem",
            json={"session_id": session_id}
        )
        problem_data = response.json()
        problem_id = problem_data["problem_id"]
        problem_text = problem_data["problem"]
        difficulty = problem_data["difficulty"]
        print(f"   ✓ Problem ID: {problem_id}")
        print(f"   Difficulty: {difficulty}")
        print(f"   Problem: {problem_text}")
    except Exception as e:
        print(f"   ✗ Failed to get problem: {e}")
        return
    
    print("\n5. Submitting a Test Solution...")
    test_solution = "42"
    try:
        response = requests.post(
            f"{agent_url}/submit_solution",
            json={
                "session_id": session_id,
                "problem_id": problem_id,
                "solution": test_solution
            }
        )
        evaluation = response.json()
        print(f"   ✓ Solution submitted: {test_solution}")
        print(f"   Score: {evaluation['score']}/100")
        print(f"   Correct: {evaluation['correct']}")
        print(f"   Feedback: {evaluation['feedback']}")
        if evaluation.get('expected_answer'):
            print(f"   Expected: {evaluation['expected_answer']}")
    except Exception as e:
        print(f"   ✗ Failed to submit solution: {e}")
        return
    
    print("\n6. Checking Session Status...")
    try:
        response = requests.get(f"{launcher_url}/session/{session_id}")
        status = response.json()
        print(f"   ✓ Problems attempted: {status['problems_attempted']}")
        print(f"   Remaining: {status['remaining']}")
    except Exception as e:
        print(f"   ✗ Failed to get session status: {e}")
        return
    
    print("\n7. Listing All Problems...")
    try:
        response = requests.get(f"{agent_url}/problems")
        problems = response.json()
        print(f"   ✓ Total problems: {problems['total']}")
        print(f"   Problem IDs: {[p['id'] for p in problems['problems']]}")
    except Exception as e:
        print(f"   ✗ Failed to list problems: {e}")
        return
    
    print("\n" + "=" * 60)
    print("A2A PROTOCOL TESTS")
    print("=" * 60)
    
    print("\n8. Testing Agent Card Endpoint...")
    try:
        response = requests.get(f"{agent_url}/.well-known/agent.json")
        agent_card = response.json()
        print(f"   ✓ Agent Name: {agent_card['name']}")
        print(f"   Schema Version: {agent_card['schema_version']}")
        print(f"   A2A Endpoint: {agent_card['versions'][0]['endpoint']}")
        print(f"   Skills: {len(agent_card['capabilities']['skills'])}")
    except Exception as e:
        print(f"   ✗ Failed to get agent card: {e}")
        return
    
    print("\n9. Testing Launcher Card Endpoint...")
    try:
        response = requests.get(f"{launcher_url}/.well-known/agent.json")
        launcher_card = response.json()
        print(f"   ✓ Launcher Name: {launcher_card['name']}")
        print(f"   A2A Endpoint: {launcher_card['versions'][0]['endpoint']}")
        print(f"   Skills: {len(launcher_card['capabilities']['skills'])}")
    except Exception as e:
        print(f"   ✗ Failed to get launcher card: {e}")
        return
    
    print("\n10. Testing A2A Start Session...")
    try:
        a2a_request = {
            "task_id": "test-task-001",
            "skill_id": "start_session",
            "messages": [
                {
                    "role": "user",
                    "content": "Start a new evaluation session"
                }
            ]
        }
        response = requests.post(f"{launcher_url}/a2a", json=a2a_request)
        a2a_response = response.json()
        print(f"   ✓ Task Status: {a2a_response['status']}")
        a2a_session_id = a2a_response['result']['session_id']
        print(f"   Session ID: {a2a_session_id}")
    except Exception as e:
        print(f"   ✗ Failed A2A start session: {e}")
        return
    
    print("\n11. Testing A2A Get Problem...")
    try:
        a2a_request = {
            "task_id": "test-task-002",
            "skill_id": "get_math_problem",
            "parameters": {
                "session_id": a2a_session_id
            },
            "messages": [
                {
                    "role": "user",
                    "content": f"Get a math problem for session {a2a_session_id}"
                }
            ]
        }
        response = requests.post(f"{agent_url}/a2a", json=a2a_request)
        a2a_response = response.json()
        print(f"   ✓ Task Status: {a2a_response['status']}")
        a2a_problem_id = a2a_response['result']['problem_id']
        a2a_problem = a2a_response['result']['problem']
        print(f"   Problem ID: {a2a_problem_id}")
        print(f"   Problem: {a2a_problem}")
    except Exception as e:
        print(f"   ✗ Failed A2A get problem: {e}")
        return
    
    print("\n12. Testing A2A Evaluate Solution...")
    try:
        a2a_request = {
            "task_id": "test-task-003",
            "skill_id": "evaluate_solution",
            "parameters": {
                "session_id": a2a_session_id,
                "problem_id": a2a_problem_id,
                "solution": "42"
            },
            "messages": [
                {
                    "role": "user",
                    "content": f"Evaluate solution: 42 for problem {a2a_problem_id}"
                }
            ]
        }
        response = requests.post(f"{agent_url}/a2a", json=a2a_request)
        a2a_response = response.json()
        print(f"   ✓ Task Status: {a2a_response['status']}")
        print(f"   Score: {a2a_response['result']['score']}/100")
        print(f"   Correct: {a2a_response['result']['correct']}")
        print(f"   Feedback: {a2a_response['result']['feedback'][:50]}...")
    except Exception as e:
        print(f"   ✗ Failed A2A evaluate solution: {e}")
        return
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓ (REST API + A2A Protocol)")
    print("\nYour agent is ready to register on AgentBeats!")
    print("Visit: https://agentbeats.org/login")
    print("\nA2A Endpoints:")
    print(f"  Agent Card:    {agent_url}/.well-known/agent.json")
    print(f"  Agent A2A:     {agent_url}/a2a")
    print(f"  Launcher Card: {launcher_url}/.well-known/agent.json")
    print(f"  Launcher A2A:  {launcher_url}/a2a")


if __name__ == "__main__":
    print("\nMake sure both servers are running:")
    print("  Terminal 1: uvicorn main:agent_app --host 0.0.0.0 --port 8000")
    print("  Terminal 2: uvicorn main:launcher_app --host 0.0.0.0 --port 8001")
    print("\nOr use: python run_agent.py")
    print("\nWaiting 3 seconds before testing...\n")
    time.sleep(3)
    test_agent()

