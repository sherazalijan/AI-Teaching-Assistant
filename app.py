
import streamlit as st
import time
import random
import tempfile
import os
from agents.professor import run_professor
from agents.advisor import run_advisor
from agents.librarian import run_librarian
from agents.assistant import run_assistant
from agents.mentor import run_mentor
from utils.safe_generate import safe_generate
from rag.rag_pipeline import RAGPipeline

# ==========================================================
# PAGE CONFIGURATION & THEME SETUP
# ==========================================================
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Premium Frosted Glass (Glassmorphism) Theme
cream_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* Main Variables and Backgrounds */
:root {
    --bg-cream-primary: #FAF7F2;
    --bg-cream-secondary: rgba(243, 236, 225, 0.6);
    --bg-glass-card: rgba(255, 255, 255, 0.45);
    --border-glass: rgba(255, 255, 255, 0.6);
    --border-gold-glass: rgba(194, 155, 104, 0.25);
    --text-charcoal: #2E251B;
    --accent-gold: #C29B68;
    --accent-gold-hover: #AF8552;
    --card-shadow: 0 8px 32px 0 rgba(194, 155, 104, 0.06);
}

/* Global Styles with Ambient Fluid Background Gradient */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(243, 236, 225, 0.8) 0%, rgba(250, 247, 242, 1) 90%) !important;
    color: #2E251B !important;
    font-family: 'Inter', sans-serif !important;
}

/* Glassmorphic Custom Header */
.hero-container {
    text-align: center;
    padding: 3.5rem 1.5rem 3rem 1.5rem;
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(20px) saturate(110%);
    -webkit-backdrop-filter: blur(20px) saturate(110%);
    border-radius: 24px;
    margin-bottom: 2.5rem;
    border: 1px solid var(--border-glass);
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(194, 155, 104, 0.05) 0%, transparent 50%);
    pointer-events: none;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #2E251B;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.15rem;
    color: #6B5E4F;
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.6;
}

.gradient-accent-bar {
    height: 3px;
    width: 80px;
    background: linear-gradient(90deg, rgba(194,155,104,0), #C29B68, rgba(194,155,104,0));
    margin: 0.5rem auto 1.5rem auto;
    border-radius: 10px;
}

/* Sidebar Frosted Glass Styling */
[data-testid="stSidebar"] {
    background: rgba(243, 236, 225, 0.5) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid var(--border-glass) !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #2E251B !important;
}

/* Premium Navigation Sidebar Layout */
.sidebar-header {
    padding: 1.5rem 1rem 1rem 1rem;
    text-align: center;
    border-bottom: 1px solid rgba(194, 155, 104, 0.15);
    margin-bottom: 1.5rem;
}

.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #2E251B;
}

.sidebar-subtitle {
    font-size: 0.8rem;
    color: #7A6D5C;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Frosted Agent Cards Grid Design */
.agent-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
}

.agent-card {
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 1.75rem;
    box-shadow: var(--card-shadow);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.agent-card:hover {
    transform: translateY(-6px);
    background: rgba(255, 255, 255, 0.55);
    box-shadow: 0 16px 36px rgba(194, 155, 104, 0.12);
    border-color: #C29B68;
}

.agent-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background-color: #C29B68;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.agent-card:hover::before {
    opacity: 1;
}

.agent-icon-container {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 1.25rem;
    border: 1px solid var(--border-glass);
}

.agent-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: #2E251B;
    margin-bottom: 0.4rem;
}

.agent-desc {
    font-size: 0.9rem;
    color: #6B5E4F;
    line-height: 1.5;
}

/* Frosted Glass PDF Upload Zone */
.upload-zone {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 2px dashed rgba(194, 155, 104, 0.4);
    border-radius: 20px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    margin-bottom: 1.5rem;
    cursor: pointer;
}

.upload-zone:hover {
    border-color: #C29B68;
    background: rgba(255, 255, 255, 0.45);
}

.upload-icon {
    font-size: 2.2rem;
    color: #C29B68;
    margin-bottom: 0.75rem;
}

.upload-text-main {
    font-weight: 500;
    color: #2E251B;
    font-size: 1.05rem;
    margin-bottom: 0.25rem;
}

.upload-text-sub {
    font-size: 0.85rem;
    color: #7A6D5C;
}

/* Frosted Chat Console Container */
.chat-container {
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.5rem;
}

.chat-bubble {
    padding: 1.2rem 1.5rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    max-width: 85%;
    line-height: 1.55;
    font-size: 0.95rem;
}

.chat-bubble-user {
    background: rgba(243, 236, 225, 0.6);
    backdrop-filter: blur(8px);
    color: #2E251B;
    margin-left: auto;
    border-bottom-right-radius: 4px;
    border: 1px solid var(--border-gold-glass);
}

.chat-bubble-ai {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(8px);
    color: #2E251B;
    margin-right: auto;
    border-bottom-left-radius: 4px;
    border: 1px solid var(--border-glass);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);
}

.chat-avatar {
    font-size: 1.2rem;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
}

/* Frosted RAG Flow Visualizer */
.rag-flow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: var(--card-shadow);
}

.rag-step {
    flex: 1;
    min-width: 140px;
    text-align: center;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    position: relative;
    transition: all 0.3s ease;
}

.rag-step.active {
    border-color: #C29B68;
    background: rgba(255, 255, 255, 0.65);
    box-shadow: 0 4px 15px rgba(194, 155, 104, 0.08);
}

.rag-step-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.rag-step-title {
    font-weight: 600;
    font-size: 0.85rem;
    color: #2E251B;
    margin-bottom: 0.2rem;
}

.rag-step-status {
    font-size: 0.75rem;
    color: #7A6D5C;
    font-family: 'JetBrains Mono', monospace;
}

.rag-arrow {
    font-size: 1.2rem;
    color: #C29B68;
    user-select: none;
}

/* Premium Error UI Cards with Frosted Backdrop */
.error-card {
    background: rgba(255, 251, 251, 0.45);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(252, 210, 210, 0.6);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(220, 53, 69, 0.03);
    border-left: 5px solid #DC3545;
}

.error-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #9C1A25;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.error-msg {
    color: #5C4A4A;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Premium Footer */
.footer-container {
    text-align: center;
    padding: 3rem 1.5rem;
    margin-top: 4rem;
    border-top: 1px solid rgba(194, 155, 104, 0.15);
}

.footer-text {
    font-size: 0.9rem;
    color: #7A6D5C;
    margin-bottom: 0.5rem;
}

.footer-sub {
    font-size: 0.8rem;
    color: #A39684;
    letter-spacing: 0.05em;
}

.pulse-indicator {
    width: 8px;
    height: 8px;
    background-color: #28A745;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7);
    }
    70% {
        transform: scale(1);
        box-shadow: 0 0 0 6px rgba(40, 167, 69, 0);
    }
    100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(40, 167, 69, 0);
    }
}
</style>
"""
st.markdown(cream_css, unsafe_allow_html=True)

# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_step' not in st.session_state:
    st.session_state.rag_step = 0
if 'pdf_uploaded' not in st.session_state:
    st.session_state.pdf_uploaded = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = ""
if 'api_working' not in st.session_state:
    st.session_state.api_working = True  # Toggle this in settings to show warning UI
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Learning Assistant"
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()

# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-title">EduAI</div>
        <div class="sidebar-subtitle">Teaching Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Elegant custom-feel sidebar radio selections
    st.markdown("##### NAVIGATION")
    nav_selection = st.radio(
        label="Go to",
        options=["🎓 Learning Assistant", "📄 PDF Chat (RAG)", "⚙ Settings", "ℹ About"],
        label_visibility="collapsed"
    )
    
    # Store clean route
    if "Learning Assistant" in nav_selection:
        st.session_state.active_tab = "Learning Assistant"
    elif "PDF Chat" in nav_selection:
        st.session_state.active_tab = "PDF Chat"
    elif "Settings" in nav_selection:
        st.session_state.active_tab = "Settings"
    else:
        st.session_state.active_tab = "About"
        
    st.markdown("---")
    
    # Sidebar status panel
    st.markdown("##### SYSTEM STATUS")
    api_status_class = "pulse-indicator" if st.session_state.api_working else ""
    api_status_label = "Gemini API: Active" if st.session_state.api_working else "Gemini API: Offline"
    api_color = "#28A745" if st.session_state.api_working else "#DC3545"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.6rem; font-size: 0.9rem; padding: 0.5rem 0;">
        <span style="width: 10px; height: 10px; background-color: {api_color}; border-radius: 50%; display: inline-block;"></span>
        <span>{api_status_label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.pdf_uploaded:
        st.markdown(f"""
        <div style="background-color: rgba(194, 155, 104, 0.06); border: 1px solid rgba(194, 155, 104, 0.15); border-radius: 12px; padding: 0.8rem; margin-top: 1rem;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #7A6D5C; letter-spacing: 0.05em; font-weight: 600;">Active Context</div>
            <div style="font-size: 0.85rem; font-weight: 500; margin-top: 0.2rem; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">📄 {st.session_state.pdf_name}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# MAIN APP BODY
# ==========================================================

# 1. HERO HEADER SECTION
st.markdown("""
<div class="hero-container">
    <div class="hero-title">AI Teaching Assistant</div>
    <div class="gradient-accent-bar"></div>
    <div class="hero-subtitle">Learn, Explore, Research and Build with AI</div>
</div>
""", unsafe_allow_html=True)

# 2. CHECK API HEALTH
if not st.session_state.api_working:
    st.markdown("""
    <div class="error-card">
        <div class="error-title">⚠ AI Service Temporarily Unavailable</div>
        <div class="error-msg">
            The Gemini API quota has been reached. 
            The application is working correctly, but AI generation is temporarily unavailable. 
            Please try again later or check your API key settings.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. CHOOSE ROUTE BY TAB STATE
if st.session_state.active_tab == "Learning Assistant":
    st.markdown("### Meet Your AI Agents")
    st.markdown("Click on any premium card to launch the interaction dashboard with that specialized learning agent.")
    
    # Grid of agent cards
    st.markdown("""
    <div class="agent-grid">
        <div class="agent-card">
            <div class="agent-icon-container">📘</div>
            <div class="agent-name">Professor</div>
            <div class="agent-desc">Explains concepts and theory clearly. Specializes in breaking down complex topics into easily digestible academic lessons.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon-container">🗺️</div>
            <div class="agent-name">Academic Advisor</div>
            <div class="agent-desc">Creates personalized learning roadmaps, course pathways, and structural career milestones tailored to your goals.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon-container">📚</div>
            <div class="agent-name">Research Librarian</div>
            <div class="agent-desc">Finds academic resources, journals, papers, and formats accurate references for any subject domain.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon-container">📝</div>
            <div class="agent-name">Teaching Assistant</div>
            <div class="agent-desc">Creates interactive exercises, conceptual quizzes, practice worksheets, and provides immediate constructive grading feedback.</div>
        </div>
        <div class="agent-card">
            <div class="agent-icon-container">🚀</div>
            <div class="agent-name">Project Mentor</div>
            <div class="agent-desc">Suggests real-world coding and structural engineering projects, assists in system architecture, and reviews code.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interaction UI for the selected agent
    agents = {
        "Professor": "📘 Professor",
        "Academic Advisor": "🗺️ Academic Advisor",
        "Research Librarian": "📚 Research Librarian",
        "Teaching Assistant": "📝 Teaching Assistant",
        "Project Mentor": "🚀 Project Mentor"
    }
    
    selected_agent_name = st.selectbox(
        "Launch Agent Terminal:", 
        options=list(agents.keys()),
        index=0
    )
    
    st.markdown(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #EAE3D2; border-radius: 20px; padding: 2rem; box-shadow: var(--card-shadow);">
        <h4 style="margin-top:0; font-family: 'Playfair Display', serif; color: #2E251B; display: flex; align-items: center; gap: 0.5rem;">
            <span>{agents[selected_agent_name].split()[0]}</span> {selected_agent_name} Console
        </h4>
        <p style="color: #6B5E4F; font-size: 0.95rem; margin-bottom: 1.5rem;">
            Ask any academic question, request a lesson, or seek feedback. The specialized agent prompt context is loaded automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick interaction chat box
    agent_input = st.text_input(f"Send a message to {selected_agent_name}:", placeholder="E.g., Explain Quantum Computing in simple terms...")
    if st.button("Generate Answer", key="btn_agent_gen"):
        if agent_input:
            if not st.session_state.api_working:
                st.error("AI Generation is temporarily locked due to API Quota limits. Check your health settings.")
            else:
                with st.spinner("Agent compiling response..."):
                    if selected_agent_name == "Professor":
                        response = safe_generate(run_professor, agent_input)
                    elif selected_agent_name == "Academic Advisor":
                        response = safe_generate(run_advisor, agent_input)
                    elif selected_agent_name == "Research Librarian":
                        response = safe_generate(run_librarian, agent_input)
                    elif selected_agent_name == "Teaching Assistant":
                        response = safe_generate(run_assistant, agent_input)
                    else:
                        response = safe_generate(run_mentor, agent_input)

                    st.markdown("##### Response:")
                    st.markdown(response)

elif st.session_state.active_tab == "PDF Chat":
    st.markdown("### Document Ingestion & RAG Workspace")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Document Upload")
        
        # Styled PDF Upload Drag and Drop box
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">📄</div>
            <div class="upload-text-main">Drag and drop your learning PDF here</div>
            <div class="upload-text-sub">Supports textbooks, slides, research papers (Max 50MB)</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
        
        if uploaded_file:
            st.session_state.pdf_uploaded = True
            st.session_state.pdf_name = uploaded_file.name
            
            with st.spinner("Extracting text and generating embeddings..."):
                # Write uploaded bytes to a temporary file on disk
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Pass to your real backend
                st.session_state.rag_pipeline.ingest_pdf(tmp_file_path)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
            
            # Show upload status
            st.success(f"Successfully processed and embedded: {uploaded_file.name}")
            
            if st.session_state.rag_step == 0:
                st.session_state.rag_step = 3
                
        # Action steps control to showcase pipeline
        st.markdown("#### Simulation Controls")
        st.write("Advance the pipeline steps to test the beautifully rendered visual state dashboard below:")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("Advance Step ➔"):
                st.session_state.rag_step = min(st.session_state.rag_step + 1, 5)
        with col_s2:
            if st.button("Reset Steps ↺"):
                st.session_state.rag_step = 0
                
    with col2:
        st.markdown("#### RAG Context Visualizer")
        
        # Steps descriptions
        steps = [
            {"icon": "📄", "title": "PDF Loaded", "status": "PENDING"},
            {"icon": "✂", "title": "Chunks Created", "status": "PENDING"},
            {"icon": "🧠", "title": "Embeddings", "status": "PENDING"},
            {"icon": "🔎", "title": "Context Retrieved", "status": "PENDING"},
            {"icon": "🤖", "title": "Answer Generated", "status": "PENDING"}
        ]
        
        # Update statuses based on current simulation state
        if st.session_state.rag_step >= 1:
            steps[0]["status"] = "ACTIVE" if st.session_state.rag_step == 1 else "SUCCESS"
        if st.session_state.rag_step >= 2:
            steps[1]["status"] = "ACTIVE" if st.session_state.rag_step == 2 else "SUCCESS"
        if st.session_state.rag_step >= 3:
            steps[2]["status"] = "ACTIVE" if st.session_state.rag_step == 3 else "SUCCESS"
        if st.session_state.rag_step >= 4:
            steps[3]["status"] = "ACTIVE" if st.session_state.rag_step == 4 else "SUCCESS"
        if st.session_state.rag_step >= 5:
            steps[4]["status"] = "ACTIVE" if st.session_state.rag_step == 5 else "SUCCESS"
            
        # Draw RAG Flow
        # Draw RAG Flow
        step_htmls = []
        for i, s in enumerate(steps):
            active_class = "active" if s["status"] in ["ACTIVE", "SUCCESS"] else ""
            status_color = "#C29B68" if s["status"] == "ACTIVE" else ("#28A745" if s["status"] == "SUCCESS" else "#A39684")
            
            # THE f""" AND """ ARE REQUIRED BY PYTHON
            step_htmls.append(f"""
<div class="rag-step {active_class}">
<div class="rag-step-icon">{s['icon']}</div>
<div class="rag-step-title">{s['title']}</div>
<div class="rag-step-status" style="color: {status_color};">{s['status']}</div>
</div>
""")
            
        # THE f""" AND """ ARE REQUIRED BY PYTHON
        flow_content = f"""
<div class="rag-flow">
{step_htmls[0]}
<div class="rag-arrow">➔</div>
{step_htmls[1]}
<div class="rag-arrow">➔</div>
{step_htmls[2]}
<div class="rag-arrow">➔</div>
{step_htmls[3]}
<div class="rag-arrow">➔</div>
{step_htmls[4]}
</div>
"""
        st.markdown(flow_content, unsafe_allow_html=True)
        
        # Modern Chat Interface (ChatGPT lookalike)
        st.markdown("#### ChatGPT-Style RAG Chat Console")
        
        # Render conversation history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Prepopulate dialogue for demonstration if empty
        if len(st.session_state.messages) == 0:
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome! Please upload your textbook or lecture notes PDF, and we can begin our contextual learning session."},
            ]
            
        for msg in st.session_state.messages:
            bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            avatar = "👤 Student" if msg["role"] == "user" else "🤖 EduAI"
            
            st.markdown(f"""
            <div class="chat-bubble {bubble_class}">
                <div class="chat-avatar">{avatar}</div>
                <div>{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Question input area
        user_question = st.text_input("Ask a question about your PDF documents:", placeholder="E.g., What are the core theories mentioned in chapter 3?", key="rag_chat_input")
        
        if st.button("Send Message ➔", key="btn_send_rag_chat"):
            if user_question:
                if not st.session_state.pdf_uploaded:
                    st.warning("Please upload a PDF document first in the sidebar or upload zone to supply appropriate local context.")
                else:
                    # Append user message
                    st.session_state.messages.append({"role": "user", "content": user_question})
                    
                    # Advance state
                    st.session_state.rag_step = 5
                    
                    with st.spinner("Querying vector index & retrieving key contexts..."):
                        try:
                            ai_response = st.session_state.rag_pipeline.query(user_question)
                        except Exception as e:
                            ai_response = f"RAG Query Error: {str(e)}"
                            
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        st.rerun()

elif st.session_state.active_tab == "Settings":
    st.markdown("### UI Theme & System Settings")
    st.markdown("Customize your interactive AI Teaching Assistant dashboard below.")
    
    st.session_state.api_working = st.checkbox("Simulate Live API Health State (Uncheck to trigger Error Warning UI)", value=st.session_state.api_working)
    
    st.markdown("#### Environment Configuration")
    st.text_input("Gemini API Key:", type="password", value="••••••••••••••••••••••••", disabled=True)
    st.caption("API keys are managed securely in your deployment settings to keep backend secrets locked.")
    
    st.markdown("#### System Settings")
    chunk_size = st.slider("Text Chunk Size (Characters)", min_value=200, max_value=2000, value=500, step=100)
    chunk_overlap = st.slider("Chunk Overlap", min_value=10, max_value=200, value=50, step=10)
    
    st.success("Configured properties cached successfully.")

else:  # About tab
    st.markdown("### About AI Teaching Assistant")
    st.markdown("""
    The **AI Teaching Assistant** is a high-performance agentic learning architecture. It utilizes advanced RAG (Retrieval-Augmented Generation) technology alongside multi-agent expert systems to deliver customized textbooks tutoring, roadmap pathing, and academic support.
    
    ##### Architectural Highlights
    - **Vector Indexes**: Chunks text documents locally and structures them in dynamic vector search pipelines.
    - **Expert Agents Orchestration**: Leverages localized persona prompts to deliver tailored consultations (e.g. Professor, Research Librarian).
    - **Soft Cream Palette UX**: Designed specifically with high contrast, calm, eye-safe cream tones to reduce visual stress during long study sessions.
    
    ##### Core System Features
    - Chat logs with ChatGPT styling
    - Immediate RAG pipeline stages visualizer
    - Interactive agent desks
    - Fully responsive layouts
    """)

# ==========================================================
# FOOTER SECTION
# ==========================================================
st.markdown("""
<div class="footer-container">
    <div class="footer-text">Made with ❤️ by <b>Sheraz Ali Jan (Maverick)</b></div>
    <div class="footer-sub">AI Teaching Assistant • Agentic AI • RAG Systems • Generative AI</div>
</div>
""", unsafe_allow_html=True)
