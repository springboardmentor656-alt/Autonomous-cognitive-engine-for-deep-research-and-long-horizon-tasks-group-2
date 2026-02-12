import os
import json
import argparse
from langgraph.graph import StateGraph
from agent import planner, executor
from state import AgentState

def compile_app():
    graph = StateGraph(AgentState)
    graph.add_node("plan", planner)
    graph.add_node("execute", executor)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")
    graph.set_finish_point("execute")
    return graph.compile()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_experiment(dataset_path, experiment_id, out_dir="experiments"):
    app = compile_app()
    ensure_dir(out_dir)
    results_dir = os.path.join(out_dir, experiment_id, "results")
    ensure_dir(results_dir)
    metrics = []

    with open(dataset_path, "r", encoding="utf-8") as fh:
        for line in fh:
            item = json.loads(line)
            task_id = item.get("id") or item.get("task_id") or f"task_{len(metrics)+1}"
            task_prompt = item.get("prompt") or item.get("text") or item.get("task")

            state = {
                "messages": [],
                "todos": [],
                "files": {},
                "dataset_item": task_prompt,
                "experiment_id": experiment_id,
                "task_id": task_id,
                "metrics": {}
            }
            result = app.invoke(state)
            final_text = result["files"].get("final_report.txt", "")
            out_file = os.path.join(results_dir, f"{task_id}.txt")
            with open(out_file, "w", encoding="utf-8") as outfh:
                outfh.write(final_text)
            # compute simple completion metric
            todos = result.get("todos", [])
            completed = sum(1 for t in todos if t.get("status") == "done")
            total = len(todos)
            metrics.append({
                "task_id": task_id,
                "completed_steps": completed,
                "total_steps": total,
                "final_path": out_file
            })
            print(f"Ran {task_id} -> saved {out_file}")

    # save metrics
    metrics_path = os.path.join(out_dir, experiment_id, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as mh:
        json.dump(metrics, mh, indent=2)
    print("Experiment finished. Metrics saved to", metrics_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True, help="path to tasks jsonl")
    p.add_argument("--experiment", required=True, help="experiment id, e.g. exp-001")
    args = p.parse_args()
    run_experiment(args.dataset, args.experiment)