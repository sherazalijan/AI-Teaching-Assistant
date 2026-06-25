from utils.gemini_client import model
from utils.gemini_client import safe_generate_content

def run_advisor(topic, knowledge_base=None, length_instruction=None):
    if length_instruction is None:
        length_instruction = "Default instruction for safe output"

    prompt = f"""
You are a world-class academic advisor.

Topic:
{topic}

Knowledge Base:
{knowledge_base}

Instructions:
{length_instruction}

Create:

# Beginner Stage
# Intermediate Stage
# Advanced Stage
# Expert Stage
"""

    

    return safe_generate_content(prompt)