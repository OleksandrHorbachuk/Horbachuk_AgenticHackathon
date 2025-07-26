# src/main.py
import planner
import executor
import sys

def run_agentic_app():
    """
    The main logic of our Agentic AI application, optimized for fewer API calls.
    """
    print("Hello! Welcome to the Color-Mood Analyzer Agent.")
    
    user_text = input("Please enter the text you want to analyze: ")
    if not user_text.strip():
        print("Text cannot be empty. Exiting.")
        sys.exit()
    
    print("\nAgent started...")
    
    context = {
        "original_text": user_text,
        "previous_results": []
    }
    
    # Step 1: Planning
    plan = planner.plan_task(user_text)
    print("\n--- Generated Plan ---")
    for step in plan:
        print(step)
    
    # Step 2: Execution
    print("\n--- Execution Started ---")
    
    for step in plan:
        result = executor.execute_step(step, context)
        
        if '[Synthesize]' in step:
            print("\n--- Final Report ---")
            print(result)
            break
        
        context["previous_results"].append(result)

if __name__ == "__main__":
    run_agentic_app()