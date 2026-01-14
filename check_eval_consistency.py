
from agent.evaluators import PlanEvaluator
import os
from dotenv import load_dotenv

load_dotenv()

evaluator = PlanEvaluator()
try:
    print(f"Using Provider: {os.getenv('PRIMARY_LLM_PROVIDER')}")
    res = evaluator.evaluate("Test task", ["Step 1", "Step 2"])
    print("Evaluation Success:", res)
except Exception as e:
    print("Evaluation Failed:", e)
