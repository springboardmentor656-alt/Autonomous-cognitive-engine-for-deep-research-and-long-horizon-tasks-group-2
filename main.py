import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langsmith import traceable

# 1. Load API Keys
load_dotenv() 
if not os.environ.get("GROQ_API_KEY"):
    print("❌ ERROR: GROQ_API_KEY not found in .env")

# Import your agent components
from agent import planner, executor
from state import AgentState

# 2. Define the Graph Workflow
graph = StateGraph(AgentState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", END) 

app = graph.compile()

@traceable(name="Autonomous Research Agent")
def run_agent(initial_state):
    # Milestone 2: Thread_id ensures persistence across turns
    config = {"configurable": {"thread_id": initial_state["task_id"]}}
    return app.invoke(initial_state, config=config)

def save_experiment_results(result, initial_state):
    """
    MILESTONE 4: Physical Persistence for Evaluation.
    Saves reports and logs to the 'experiments' folder.
    """
    exp_id = initial_state.get("experiment_id", "exp_001")
    task_id = initial_state.get("task_id", "task_001")
    
    # Create directory: experiments/exp_001/results/
    base_path = os.path.join("experiments", exp_id)
    results_path = os.path.join(base_path, "results")
    os.makedirs(results_path, exist_ok=True)

    # 1. Save the Final Report as a .txt file
    report_content = result["files"].get("final_report.txt", "No report generated.")
    report_filename = f"{task_id}_final_report.txt"
    with open(os.path.join(results_path, report_filename), "w", encoding="utf-8") as f:
        f.write(report_content)

    # 2. Update metrics.json (Required for evaluate_experiment.py)
    metrics_file = os.path.join(base_path, "metrics.json")
    all_metrics = []
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            all_metrics = json.load(f)

    # Add this run's data to the metrics
    all_metrics.append({
        "task_id": task_id,
        "topic": initial_state["dataset_item"],
        "timestamp": datetime.now().isoformat(),
        "final_path": os.path.join(results_path, report_filename), # Link for the judge
        "quality_score": 0  # To be filled by evaluate_experiment.py
    })

    with open(metrics_file, "w") as f:
        json.dump(all_metrics, f, indent=4)

    print(f"\n✅ Milestone 4: Results logged to {base_path}")

if __name__ == "__main__":
    # Get topic from command line or use default
    task_input = sys.argv[1] if len(sys.argv) > 1 else "AI in Healthcare Data Privacy"
    
    # Generate a unique task ID per run (e.g., T1, T2, T3)
    # This ensures your results don't overwrite each other
    t_id = f"task_{datetime.now().strftime('%M%S')}"

    initial_state = {
        "messages": [],
        "todos": [],        # Milestone 1: Planner fills this
        "files": {},        # Milestone 2: Virtual File System
        "dataset_item": task_input,
        "experiment_id": "exp_001",
        "task_id": t_id,
        "metrics": {}
    }

    print(f"🚀 Starting Engine | Task: {task_input} | ID: {t_id}\n")
    
    try:
        # Run the agent
        final_result = run_agent(initial_state)

        # Print Output to Terminal
        if "final_report.txt" in final_result["files"]:
            print("\n=== FINAL REPORT GENERATED ===")
            print(final_result["files"]["final_report.txt"][:500] + "...") 
        
        # PERSIST DATA FOR EVALUATION
        save_experiment_results(final_result, initial_state)
            
    except Exception as e:
        print(f"❌ Execution failed: {e}")