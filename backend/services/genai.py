from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", api_key)
# Create client
client = OpenAI(api_key=api_key)


# 🔥 MAIN FUNCTION (THIS WAS MISSING OR BROKEN)
def generate_ai_plan(plan):
    response = ""

    for item in plan:
        response += f"""
📘 Study: {item['topic']} ({item['subject']})
→ Reason: Low confidence ({item['confidence']}) and high priority
→ Tip: Practice questions and revise key concepts

"""

    return response