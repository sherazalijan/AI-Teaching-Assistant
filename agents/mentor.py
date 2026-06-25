from utils.gemini_client import model

def run_mentor(topic, knowledge_base=None, length_instruction=None):
    if length_instruction is None:
        length_instruction = "Default instruction for safe output"
    prompt = f"""
You are a senior AI project mentor.

Topic:
{topic}

Knowledge Base:
{knowledge_base}

Instructions:
{length_instruction}

Create:

# Beginner Projects
# Intermediate Projects
# Advanced Projects
# Portfolio Projects
"""

    response = model.generate_content(prompt)

    return f"[MOCK OUTPUT] Topic received: {topic}"