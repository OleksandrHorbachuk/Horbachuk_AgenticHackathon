# src/executor.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash-lite')

def colorizer_tool(instruction, text_to_analyze):
    """
    Associates each word in a text with a single color.
    """
    print(f"Executing [Colorizer] tool for: '{text_to_analyze}'...")
    prompt = f"""
    You are a creative word-to-color association tool. Your task is to associate each word in the following text with a single, common color that best fits its meaning or mood.
    The output should be a simple, comma-separated list of colors, in the same order as the words in the original text.
    Do not include the original words, just the colors. Do not include any explanations.
    
    Text to analyze: "{text_to_analyze}"
    
    Example:
    Text: "The sky is blue"
    Output: "Blue, Blue, Blue"
    
    Text to analyze: "{text_to_analyze}"
    
    Output:
    """
    try:
        response = model.generate_content(prompt)
        # Ensure output is a simple, comma-separated string
        return ", ".join([c.strip().capitalize() for c in response.text.strip().split(',')])
    except Exception as e:
        return f"Error with Colorizer Tool: {e}"

def sentiment_analyzer_tool(instruction, colors_list):
    """
    Determines the overall sentiment of a text based on a list of colors.
    """
    print(f"Executing [SentimentAnalyzer] tool for colors: '{colors_list}'...")
    prompt = f"""
    You are a sentiment analyzer. Your task is to determine the overall mood or sentiment of a text, based on the following list of associated colors.
    Provide a single word or a short phrase (e.g., "Positive", "Melancholic", "Energetic") to describe the overall mood.
    Do not provide any explanations, just the sentiment.
    
    List of colors: "{colors_list}"
    
    Overall sentiment:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with SentimentAnalyzer Tool: {e}"

def synthesize_tool(data_to_synthesize, original_text):
    """
    Combines the original text, the color list, and the sentiment into a final report.
    """
    print(f"Executing [Synthesize] tool...")
    
    # Extract the color list and sentiment from the list of results
    color_list = data_to_synthesize[0]
    sentiment = data_to_synthesize[1]
    
    prompt = f"""
    You are an expert agent. Create a final report based on the following information.
    Start by stating the original text.
    Then, list the associated colors.
    Finally, state the determined overall mood.
    Be concise and professional.
    
    Original Text: "{original_text}"
    Associated Colors: {color_list}
    Overall Mood: {sentiment}
    
    Final Report:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error with Synthesize Tool: {e}"

def execute_step(step, context):
    """
    Executes a single step by choosing the right tool based on the plan.
    """
    tool_match = re.search(r'\[(.*?)\]', step)
    
    if not tool_match:
        return "Invalid plan step format. No tool found."
    
    tool_name = tool_match.group(1).strip()
    
    print(f"Executing step with tool: [{tool_name}]")
    
    if tool_name == 'Colorizer':
        return colorizer_tool(step, context['original_text'])
    elif tool_name == 'SentimentAnalyzer':
        colors_list = context['previous_results'][0]
        return sentiment_analyzer_tool(step, colors_list)
    elif tool_name == 'Synthesize':
        return synthesize_tool(context['previous_results'], context['original_text'])
    else:
        return f"Unknown tool: {tool_name}"