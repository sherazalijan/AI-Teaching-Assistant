from utils.gemini_client import model

def run_assistant(topic, knowledge_base):

    prompt = f"""
You are an expert teaching assistant.

Topic:
{topic}

Knowledge Base:
{knowledge_base}

Create:

# Beginner Exercises

# Intermediate Exercises

# Advanced Exercises

# Quiz

# Mini Projects

# Portfolio Projects

Provide solutions and explanations.
"""

    response = model.generate_content(prompt)

    return response.text