# AI Teaching Assistant

AI Teaching Assistant is a multi-agent learning platform that combines Retrieval-Augmented Generation (RAG) with specialized AI agents to help students learn technical topics, explore resources, practice concepts, and discover project ideas.

The system supports both topic-based learning and document-based question answering through uploaded PDF files.

## Features

### Multi-Agent Learning System

The platform includes several specialized agents:

#### Professor

Explains concepts, theories, and technical topics in a structured and understandable way.

#### Academic Advisor

Creates learning roadmaps and study plans for a given topic.

#### Research Librarian

Suggests books, papers, courses, and other learning resources.

#### Teaching Assistant

Generates exercises, quizzes, and practice questions.

#### Project Mentor

Suggests practical projects and implementation ideas related to a topic.

---

## PDF Question Answering

Users can upload PDF documents and ask questions about their contents.

The system:

1. Extracts text from PDFs
2. Splits text into chunks
3. Generates embeddings
4. Stores embeddings in a vector index
5. Retrieves relevant context
6. Generates answers using Gemini

This allows responses to be grounded in the uploaded document rather than relying only on the language model.

---

## System Architecture

### Agent Workflow

User Query

↓

Selected Agent

↓

Prompt Construction

↓

Gemini API

↓

Generated Response

### RAG Workflow

PDF Upload

↓

Text Extraction

↓

Chunking

↓

Embedding Generation

↓

Vector Store

↓

Context Retrieval

↓

Gemini Response

---

## Technologies Used

### Frontend

* Streamlit

### Backend

* Python

### AI

* Google Gemini API

### RAG Components

* PyPDF
* Custom Text Chunking
* Vector Retrieval System
* Embedding Pipeline

---

## Project Structure

AI-Teaching-Assistant/

├── agents/

│ ├── professor.py

│ ├── advisor.py

│ ├── librarian.py

│ ├── assistant.py

│ └── mentor.py

│

├── rag/

│ ├── pdf_loader.py

│ ├── text_splitter.py

│ ├── embeddings.py

│ ├── vector_store.py

│ └── rag_pipeline.py

│

├── utils/

│ ├── gemini_client.py

│ └── safe_generate.py

│

├── app.py

├── requirements.txt

└── README.md

---

## Installation

Clone the repository:

git clone <repository-url>

cd AI-Teaching-Assistant

Create a virtual environment:

python -m venv venv

Activate the environment:

macOS/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a `.env` file:

GOOGLE_API_KEY=your_api_key_here

Run the application:

streamlit run app.py

---

## Example Use Cases

* Learning Machine Learning
* Learning Deep Learning
* Exam Preparation
* Interview Preparation
* Research Paper Exploration
* Technical Concept Revision
* PDF-based Question Answering

---

## Future Improvements

* Conversation Memory
* Multi-PDF Retrieval
* Citation Support
* Persistent Chat History
* Advanced Vector Databases
* Voice Interaction

---

## Author

Sheraz Ali Jan (Maverick)

Computer Science Student interested in Machine Learning, Deep Learning, NLP, Agentic AI, and Retrieval-Augmented Generation systems.
