from utils.gemini_client import safe_generate_content

def run_professor(topic, knowledge_base=None, length_instruction=None):

    if length_instruction is None:
        length_instruction = "Provide a concise explanation."

    prompt = f"""
You are an expert university professor.

Topic:
{topic}

Instructions:
{length_instruction}

Create:

# Beginner Explanation

# Core Concepts

# Intermediate Concepts

# Advanced Concepts

# Real World Applications

# Common Mistakes

# Summary

Use markdown formatting.
"""

    return safe_generate_content(prompt)