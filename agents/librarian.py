from utils.gemini_client import model

def run_librarian(topic, knowledge_base):

    prompt = f"""
You are an expert research librarian.

Topic:
{topic}

Knowledge Base:
{knowledge_base}

Create:

# Best Books

# Best Courses

# Best YouTube Channels

# Best Documentation

# GitHub Repositories

# Research Papers

Provide links and explanations.
"""

    response = model.generate_content(prompt)

    return response.text