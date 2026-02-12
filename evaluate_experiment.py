import os
import json
import argparse
from langsmith import traceable

try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnableSequence
    HAS_LLM = True
except Exception:
    HAS_LLM = False

def simple_score(text):
    if not text or len(text.strip()) < 50:
        return 2
    score = min(10, max(1, len(text.split()) // 50 + 3))
    return score

@traceable(name="LLM_Judge_Evaluation")
def judge_with_llm(report_text):
    """
    Upgraded Judge: Evaluates based on Milestone 4 Quality Criteria.
    """
    prompt = PromptTemplate.from_template(
        "You are an expert Research Quality Auditor. Grade the following report on a scale of 1-10.\n"
        "Criteria:\n"
        "1. Does it have a clear Summary and Analysis?\n"
        "2. Is the tone academic and professional?\n"
        "3. Is the content logical and relevant?\n\n"
        "Report Content:\n{text}\n\n"
        "Respond ONLY with a JSON object in this format: "
        "{{\"score\": <number>, \"reasoning\": \"<short_explanation>\"}}"
    )
    
    # Using Llama 3 for fast, smart grading
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    chain = prompt | llm
    
    try:
        result = chain.invoke({"text": report_text})
        content = result.content
        # Extract the JSON or the number
        data = json.loads(content)
        return int(data["score"])
    except Exception:
        # Fallback to simple number extraction if JSON fails
        import re
        numbers = re.findall(r'\d+', content)
        return int(numbers[0]) if numbers else 5

def evaluate(experiment_id, base_dir="experiments"):
    # This matches the folder structure created during your runs
    results_dir = os.path.join(base_dir, experiment_id, "results")
    metrics_path = os.path.join(base_dir, experiment_id, "metrics.json")
    
    if not os.path.exists(metrics_path):
        print(f"❌ No metrics found for {experiment_id}")
        return

    with open(metrics_path, "r", encoding="utf-8") as mh:
        metrics = json.load(mh)

    scores = []
    print(f"\n--- Starting Evaluation for {experiment_id} ---")
    
    for m in metrics:
        # Check if the file actually exists in state/disk
        filename = "final_report.txt"
        # In a real setup, you'd pull this from result['files']
        # For this script, we assume you saved it in the results_dir
        path = os.path.join(results_dir, f"{m['task_id']}_final_report.txt")
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as rf:
                text = rf.read()
            
            score = judge_with_llm(text) if HAS_LLM else simple_score(text)
            m["quality_score"] = score
            scores.append(score)
            print(f"ID: {m['task_id']} | Quality Score: {score}/10")
        else:
            print(f"⚠️ Report not found for {m['task_id']}")

    if scores:
        avg = sum(scores) / len(scores)
        success_rate = sum(1 for s in scores if s >= 7) / len(scores) * 100
        print(f"\n--- FINAL RESULTS ---")
        print(f"Average Quality Score: {avg:.2f}")
        print(f"Success Rate (Score >= 7): {success_rate:.1f}%")
        
        if success_rate >= 70:
            print("✅ Milestone 4 Success Criteria Met!")
        else:
            print("❌ Success Criteria Not Met. Refine your agent prompts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_id", default="exp_001")
    args = parser.parse_args()
    evaluate(args.experiment_id)