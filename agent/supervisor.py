import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable
from tools.planning import write_todos
from tools.filesystem import write_file, read_file, edit_file, ls

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

@traceable(name="execute_todo")
def execute_todo(state, todo_item: str, todo_index: int):
    
    # REASON: Plan how to execute this TODO
    system_prompt = """
You are a task execution agent. 
Your job is to execute a specific task step and provide a clear result.

Guidelines:
- Execute the task provided
- Be thorough and comprehensive
- Output clear, structured results
- Consider any provided context from previous steps

Return only the execution result, no explanations."""
    
    # Gather context from previous TODO results
    context = ""
    previous_todos = []
    for i in range(1, todo_index):
        prev_result_file = f"todo_{i}_result.txt"
        if prev_result_file in state["files"]:
            prev_result = state["files"][prev_result_file]
            previous_todos.append(f"Step {i}: {prev_result[:200]}...")
    
    if previous_todos:
        context = f"\n\nContext from previous steps:\n" + "\n".join(previous_todos)
    
    # ACT: Use LLM to execute the TODO
    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Thinking",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Execute this task: {todo_item}{context}"}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    raw_choice = response.choices[0] if response and getattr(response, "choices", None) else None
    content = raw_choice.message.content if raw_choice and getattr(raw_choice, "message", None) else None
    result = content.strip() if content else "Model returned empty content."
    
    # OBSERVE & UPDATE: Save result to file system
    result_filename = f"todo_{todo_index}_result.txt"
    write_file(state, result_filename, result)
    
    # Save notes with context linking
    notes = f"TODO {todo_index}: {todo_item}\n\nExecution Result:\n{result}"
    notes_filename = f"todo_{todo_index}_notes.txt"
    write_file(state, notes_filename, notes)
        
    return state

@traceable(name="supervisor_agent")
def supervisor_agent(user_input: str):
    """
    Main supervisor agent that coordinates task planning and execution.
    
    Workflow:
    1. PLAN: Break down user input into TODOs
    2. EXECUTE LOOP: For each TODO, reason and act
    3. SYNTHESIZE: Gather results and create summary
    """
    
    state = {
        "input": user_input,
        "todos": [],
        "completed_todos": [],
        "status": "planning",
        "files": {}
    }

    # STEP 1: PLAN - Decompose task into TODOs
    
    print("Agent reasoning: planning required.")
    
    todos = write_todos(user_input)
    state["todos"] = todos
    
    # Save TODO list
    write_file(state, "todos.txt", "\n".join([f"{i+1}. {todo}" for i, todo in enumerate(todos)]))
    
    state["status"] = "planned"
    print(f"\nCreated {len(todos)} TODOs:")
    for i, todo in enumerate(todos, 1):
        print(f"   {i}. {todo}")
    
    # STEP 2: EXECUTION LOOP - Execute each TODO
    
    for todo_index, todo_item in enumerate(todos, 1):
        # Execute the TODO
        state = execute_todo(state, todo_item, todo_index)
        state["completed_todos"].append(todo_item)
            
    state["status"] = "executed"
    
    # STEP 3: SYNTHESIZE - Create execution summary
    print("\nAll TODOs executed. Execution summary Generated.")    
    # Gather all results
    all_results = []
    for i in range(1, len(todos) + 1):
        result_file = f"todo_{i}_result.txt"
        if result_file in state["files"]:
            result_content = state["files"][result_file]
            all_results.append(f"### Step {i}: {todos[i-1]}\n{result_content}\n")
    
    # Create execution summary
    summary = f"""
EXECUTION SUMMARY
================
Task: {user_input}
Total TODOs: {len(todos)}
Completed: {len(state['completed_todos'])}
Status: {'COMPLETE' if len(state['completed_todos']) == len(todos) else 'PARTIAL'}

DETAILED RESULTS
================
""" + "\n".join(all_results)
    
    write_file(state, "execution_summary.txt", summary)
    
    state["status"] = "complete"
        
    return state
