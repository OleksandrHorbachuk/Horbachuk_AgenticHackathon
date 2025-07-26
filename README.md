Color-Mood Analyzer Agent
This AI agent analyzes the sentiment of a text by associating its words with colors. It demonstrates a multi-step agentic architecture where a "tool" generates data that is then processed by another, showcasing a creative and non-deterministic approach to AI problem-solving.

Setup and Run

    Fork the repository:
git clone https://github.com/OleksandrHorbachuk/Horbachuk_AgenticHackathon
cd Horbachuk_AgenticHackathon

    Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    Install dependencies manually:
pip install google-generativeai
pip install python-dotenv

    Configure the Gemini API:
Get your free API key from Google AI Studio.
Create a file named .env in the root directory of your project.
Add your key to the file: GOOGLE_API_KEY="YOUR_API_KEY"

    Run the agent:
python src/main.py

The program will prompt you to enter a text for analysis.