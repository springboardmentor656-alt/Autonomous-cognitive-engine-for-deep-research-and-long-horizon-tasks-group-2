import os
from dotenv import load_dotenv
from agent.planner import TaskPlanner
from agent.evaluators import PlanEvaluator
from graph.graph import app
from agent.state import create_initial_state

# Load environment variables
load_dotenv()
os.environ["LANGSMITH_PROJECT"] = "agentic-ai-infosys"

def main():
    print("="*40)
    print("🚀 Local Playground – Task Planning Agent")
    print("="*40)

    planner = TaskPlanner(model_name="llama-3.3-70b-versatile")
    evaluator = PlanEvaluator()

    while True:
        user_task = input("\n👉 Enter your task (or 'exit' to quit): ")
        if user_task.lower() in ['exit', 'quit', 'q']:
            break

        print("\n🧠 Thinking... Breaking task into steps on Groq...")
        
        # Generate the plan
        todo_list = planner.generate_todo(user_task)

        print("\n📝 GENERATED TODOs:")
        for i, step in enumerate(todo_list, 1):
            print(f"{i}. {step}")

        

if __name__ == "__main__":
    state = create_initial_state(
        task="Research BMW EV strategy"
    )

    result = app.invoke(state)

    print("\nFINAL RESULT:")
    print(result)
    main()

