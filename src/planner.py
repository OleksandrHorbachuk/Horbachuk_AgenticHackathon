# src/planner.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def plan_task(text_to_analyze):
    """
    Generates a task plan to analyze text sentiment via color association.
    """
    print(f"\nPlanning for text: '{text_to_analyze}'...")
    
    prompt = f"""
    You are an expert agent planner. Your task is to break down a user's goal into a clear, actionable list of sub-tasks.
    Each sub-task must be preceded by a tool recommendation in brackets, like this: [TOOL_NAME].
    
    Available tools are:
    [Colorizer]: Associates each word in a text with a single color.
    [SentimentAnalyzer]: Determines the overall sentiment or mood of a text based on a list of colors.
    [Synthesize]: Combines and summarizes information into a final response.
    
    User Goal: Take a piece of text, associate a color with each word, and then determine the overall sentiment based on the colors.
    
    Provide the plan as a numbered list.
    
    Example Plan:
    1. [Colorizer] Associate colors with each word in the text 'The sun is warm and bright'.
    2. [SentimentAnalyzer] Determine the overall sentiment based on the colors yellow, yellow, yellow, green, yellow.
    3. [Synthesize] Present the original text, the list of colors, and the final sentiment.
    
    Plan for the text: '{text_to_analyze}'
    """
    
    try:
        response = model.generate_content(prompt)
        plan = response.text.strip().split('\n')
        plan = [step.strip() for step in plan if step.strip() and step.strip().startswith(('1.', '2.', '3.', '4.', '5.'))]
        return plan
    except Exception as e:
        print(f"An error occurred in planner: {e}")
        return ["Could not generate a plan due to an error."]

if __name__ == "__main__":
    test_text = "The sky is gray and full of clouds"
    my_plan = plan_task(test_text)
    print("Generated plan:")
    for step in my_plan:
        print(step)