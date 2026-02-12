from summarizer import summarize
from langsmith import traceable

# The @traceable decorator ensures this sub-task shows up 
# as a nested step in your LangSmith dashboard.
@traceable(name="Summarization_SubAgent", run_type="chain")
def task(text):
    """
    Milestone 3: Specialized delegation tool.
    Acts as a bridge between the Executor and the Summarizer Sub-Agent.
    """
    print(f"--- [DELEGATION] Spawning Summarizer Sub-Agent ---")
    
    # We use a loop for retries to ensure robustness (Requirement for Long-Horizon tasks)
    for i in range(3):
        try:
            # We pass a clean prompt to ensure the Sub-Agent knows its isolated role
            # This prevents the "Instruction Loop" error you had earlier.
            system_instruction = (
                "You are a specialized Research Assistant. "
                "Provide a concise academic summary of the text below. "
                "Do NOT include conversational filler or repeat these instructions.\n\n"
            )
            
            # Combine instruction with the actual research data
            full_input = system_instruction + text
            
            out = summarize(full_input)
            
            # Validation: Ensure the sub-agent actually returned content
            if out and len(out.strip()) > 0:
                print(f"[SUCCESS] Sub-Agent returned {len(out)} characters.")
                return out.strip()
                
        except Exception as e:
            print(f"[RETRY {i+1}] Sub-Agent delegation failed: {e}")

    # Fallback if all 3 attempts fail
    return "[Error] Sub-agent failed to provide a summary after 3 attempts."