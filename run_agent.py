import multiprocessing
import uvicorn
import time


def run_agent_server():
    uvicorn.run("main:agent_app", host="0.0.0.0", port=8000, log_level="info")


def run_launcher_server():
    uvicorn.run("main:launcher_app", host="0.0.0.0", port=8001, log_level="info")


if __name__ == "__main__":
    print("Starting Math Evaluator Green Agent...")
    print("=" * 60)
    print("\nAgent Server:    http://localhost:8000")
    print("Launcher Server: http://localhost:8001")
    print("\nPress Ctrl+C to stop both servers\n")
    print("=" * 60)
    
    agent_process = multiprocessing.Process(target=run_agent_server)
    launcher_process = multiprocessing.Process(target=run_launcher_server)
    
    try:
        agent_process.start()
        time.sleep(1)
        launcher_process.start()
        
        agent_process.join()
        launcher_process.join()
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        agent_process.terminate()
        launcher_process.terminate()
        agent_process.join()
        launcher_process.join()
        print("Servers stopped.")

