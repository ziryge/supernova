"""
SuperNova AI - Streamlit UI for the agent workflow with thinking process visualization.
"""

import os
import streamlit as st
from dotenv import load_dotenv
import time
import json
import hashlib
import random
from datetime import datetime

# Import for code editor
from streamlit_ace import st_ace

# Import authentication configuration
from auth_config import ENABLE_AUTH, USERS, SECRET_KEY

# Import custom UI components
try:
    from src.ui import (
        custom_header, card, info_card, loading_animation,
        thinking_visualization, progress_bar, tabs_with_icons,
        code_editor, collapsible_section, status_indicator,
        chat_message_enhanced, file_card, link_card,
        thinking_step, load_css_and_js
    )
    CUSTOM_UI_AVAILABLE = True
except ImportError:
    CUSTOM_UI_AVAILABLE = False

from src.workflow import run_agent_workflow
from src.config.env import DEBUG

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="SuperNova AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configure authentication
if ENABLE_AUTH:
    st.session_state.setdefault('authenticated', False)

    # Set the session state key
    if 'key' not in st.session_state:
        st.session_state['key'] = SECRET_KEY

    def authenticate(username, password):
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            return True
        return False

    # Authentication form
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>SuperNova AI Login</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Please log in to access SuperNova AI</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

                if submit:
                    if authenticate(username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        # Stop execution if not authenticated
        st.stop()

# Add custom CSS for ChatGPT-like dark theme
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #0f0f0f !important;
        color: #ececf1 !important;
    }

    /* Chat container styling */
    [data-testid="stChatContainer"] {
        background-color: #343541 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
    }

    /* Chat input container */
    [data-testid="stChatInputContainer"] {
        background-color: #343541 !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc, .css-12oz5g7, .css-1oe6wy4, .css-1aehpvj, [data-testid="stSidebar"] {
        background-color: #202123 !important;
    }

    /* Make the sidebar more compact */
    .css-1544g2n {
        padding-top: 1rem !important;
    }

    /* Button styling - ChatGPT style */
    .stButton > button {
        background-color: #10a37f !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #0e8f6f !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
    }

    /* Chat input styling */
    .stChatInput, [data-testid="stChatInput"] {
        background-color: #40414f !important;
        border-radius: 0.75rem !important;
        border: none !important;
        padding: 0.5rem !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.1) !important;
    }

    /* Chat message styling */
    .stChatMessage {
        background-color: #343541 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }

    /* Fix for chat message text color */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #ececf1 !important;
    }

    /* Style for user messages */
    [data-testid="stChatMessageContent"] {
        background-color: #343541 !important;
        color: #ececf1 !important;
    }

    /* Style for AI messages */
    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #444654 !important;
        color: #ececf1 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
    }

    /* Style for chat avatars */
    .stChatMessage [data-testid="stChatMessageAvatar"] {
        background-color: #10a37f !important;
        color: white !important;
    }

    /* Style for user avatar */
    .stChatMessage.user [data-testid="stChatMessageAvatar"] {
        background-color: #343541 !important;
    }

    /* Alternating message backgrounds - ChatGPT style */
    .stChatMessage:nth-child(odd) {
        background-color: #343541 !important;
    }

    .stChatMessage:nth-child(even) {
        background-color: #444654 !important;
    }

    /* Ensure all markdown text is visible */
    .element-container div.stMarkdown p,
    .element-container div.stMarkdown li,
    .element-container div.stMarkdown h1,
    .element-container div.stMarkdown h2,
    .element-container div.stMarkdown h3,
    .element-container div.stMarkdown h4,
    .element-container div.stMarkdown h5,
    .element-container div.stMarkdown h6,
    .element-container div.stMarkdown span {
        color: #ececf1 !important;
    }

    /* Style for code blocks in chat */
    .stChatMessage pre, .stChatMessage code {
        background-color: #2d2d3a !important;
        color: #ececf1 !important;
        border-radius: 0.375rem !important;
    }

    /* Style for links in chat */
    .stChatMessage a {
        color: #10a37f !important;
        text-decoration: none !important;
    }

    .stChatMessage a:hover {
        text-decoration: underline !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #202123 !important;
        border-radius: 0.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #343541 !important;
        color: #ffffff !important;
    }
    /* Thinking step styles - ChatGPT style */
    .thinking-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .thinking-step p {
        color: #ececf1;
        margin: 0;
        line-height: 1.5;
    }
    .thinking-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }

    /* Deep thinking step styles - ChatGPT style */
    .deep-thinking-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #19c37d;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .deep-thinking-step p {
        color: #ececf1;
        margin: 0;
        line-height: 1.5;
    }
    .deep-thinking-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    .deep-thinking-step strong {
        color: #c6f6d5;
        font-weight: 600;
    }

    /* Super deep thinking step styles - ChatGPT style */
    .super-deep-thinking-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #3a3b4b;
        border-left: 3px solid #25d195;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .super-deep-thinking-step p {
        color: #ececf1;
        margin: 0;
        line-height: 1.5;
    }
    .super-deep-thinking-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    .super-deep-thinking-step strong {
        color: #d9f7be;
        font-weight: 600;
    }
    /* Planning step styles - ChatGPT style */
    .planning-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .planning-step p {
        color: #ececf1;
        margin: 0;
        line-height: 1.5;
    }
    .planning-step ol {
        color: #ececf1;
        margin-top: 0.5rem;
        margin-bottom: 0;
        padding-left: 1.5rem;
    }
    .planning-step li {
        color: #ececf1;
        margin-bottom: 0.25rem;
    }
    .planning-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    /* Execution step styles - ChatGPT style */
    .execution-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #19c37d;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .execution-step p {
        color: #ececf1;
        margin: 0 0 0.5rem 0;
        line-height: 1.5;
    }
    .execution-step strong {
        color: #a7f3d0;
        font-weight: 600;
    }
    .execution-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    /* Terminal step styles - ChatGPT style */
    .terminal-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #2d2d3a;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .terminal-step pre {
        margin: 0;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    .terminal-step code {
        color: #ececf1;
        font-size: 0.9rem;
        background-color: #2d2d3a;
    }
    .terminal-step .step-time {
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }

    /* Delegation sections - ChatGPT style */
    .delegation-reasoning {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .delegation-reasoning h4 {
        color: #a7f3d0;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
    }
    .delegation-reasoning p {
        color: #ececf1;
        margin-bottom: 0;
        line-height: 1.5;
    }

    .delegation-instructions {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #19c37d;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .delegation-instructions h4 {
        color: #a7f3d0;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
    }
    .delegation-instructions p, .delegation-instructions li, .delegation-instructions ul, .delegation-instructions ol {
        color: #ececf1;
        line-height: 1.5;
    }
    .delegation-instructions ol, .delegation-instructions ul {
        padding-left: 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .delegation-instructions li {
        margin-bottom: 0.25rem;
    }

    .delegation-guidance {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #444654;
        border-left: 3px solid #25d195;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .delegation-guidance h4 {
        color: #a7f3d0;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
    }
    .delegation-guidance p {
        color: #ececf1;
        margin-bottom: 0;
        line-height: 1.5;
    }

    .delegation-note {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .delegation-note h4 {
        color: #a7f3d0;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
    }
    .delegation-note p {
        color: #ececf1;
        margin-bottom: 0;
        line-height: 1.5;
    }
    /* Artifact cards - ChatGPT style */
    .artifact-card {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .link-card {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .link-card a {
        color: #19c37d;
        text-decoration: none;
        font-weight: 500;
    }
    .link-card a:hover {
        text-decoration: underline;
        color: #25d195;
    }
    .file-card {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .file-card code {
        background-color: #2d2d3a;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 0.85rem;
        color: #ececf1;
    }
    /* Agent header - ChatGPT style */
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        background-color: #343541;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    .agent-emoji {
        font-size: 1.75rem;
        margin-right: 0.75rem;
        color: #10a37f;
    }
    .agent-name {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ececf1;
        letter-spacing: 0.5px;
    }
    .step-time {
        font-size: 0.8rem;
        color: #8e8ea0;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    /* Plan step - ChatGPT style */
    .plan-step {
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        background-color: #343541;
        border-left: 3px solid #10a37f;
        color: #ececf1;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .completed-step {
        text-decoration: line-through;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = None

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "debug" not in st.session_state:
    st.session_state.debug = DEBUG

if "use_enhanced_browser" not in st.session_state:
    st.session_state.use_enhanced_browser = True

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# No timeout for processing
# We removed the timeout feature as requested

if "current_step" not in st.session_state:
    st.session_state.current_step = None

# Always use dark theme
st.session_state.theme = "dark"

# Initialize thinking mode
from src.workflow.thinking_process import ThinkingProcess
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = ThinkingProcess.NORMAL_THINKING

# Sidebar
with st.sidebar:
    st.title("SuperNova AI Agent")
    st.markdown("---")

    # Agent Settings
    st.markdown("---")
    st.subheader("Agent Settings")

    # Create columns for settings
    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        st.session_state.use_enhanced_browser = st.checkbox("Enhanced Browser", value=st.session_state.use_enhanced_browser,
                                                        help="Enable to use the enhanced SuperNova browser with better web research capabilities")

    with settings_col2:
        st.session_state.debug = st.checkbox("Debug Mode", value=st.session_state.debug,
                                          help="Enable to see detailed debug information")

    # Thinking Mode selection
    st.subheader("Thinking Mode")
    thinking_mode_options = {
        ThinkingProcess.NORMAL_THINKING: "Normal",
        ThinkingProcess.DEEP_THINKING: "Deep Thinking",
        ThinkingProcess.SUPER_DEEP_THINKING: "Super Deep Thinking"
    }

    thinking_mode_descriptions = {
        "Normal": "Standard thinking process with basic reasoning.",
        "Deep Thinking": "Enhanced thinking with multiple perspectives and deeper analysis.",
        "Super Deep Thinking": "Comprehensive thinking with extensive analysis, alternative approaches, and edge cases."
    }

    selected_thinking_mode = st.radio(
        "Select Thinking Mode",
        list(thinking_mode_options.values()),
        index=list(thinking_mode_options.values()).index(thinking_mode_options[st.session_state.thinking_mode]),
        help="Choose how detailed the AI's thinking process should be."
    )

    # Display description of selected thinking mode
    st.caption(thinking_mode_descriptions[selected_thinking_mode])

    # Update thinking mode in session state
    for key, value in thinking_mode_options.items():
        if value == selected_thinking_mode:
            if st.session_state.thinking_mode != key:
                st.session_state.thinking_mode = key

    # Apply ChatGPT-style dark theme CSS
    st.markdown("""
    <style>
    .main {background-color: #0f0f0f !important;}
    [data-testid="stSidebar"] {background-color: #202123 !important;}
    .stTextInput > div > div > input {background-color: #40414f !important; color: #ececf1 !important; border: none !important;}
    .stSelectbox > div > div > div {background-color: #40414f !important; color: #ececf1 !important; border: none !important;}
    .stTextArea > div > div > textarea {background-color: #40414f !important; color: #ececf1 !important; border: none !important;}
    .stButton > button {background-color: #10a37f !important; color: white !important; border: none !important;}
    .stRadio > div {background-color: #202123 !important; padding: 10px !important; border-radius: 5px !important;}
    .stRadio label {color: #ececf1 !important;}
    .stRadio label span {color: #8e8ea0 !important;}
    </style>
    """, unsafe_allow_html=True)

    # Clear conversation button
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.thinking = None
        st.session_state.workflow_result = None
        st.session_state.is_processing = False
        st.session_state.current_step = None
        st.session_state.process_start_time = None
        st.rerun()

    # Reset processing state button (in case the UI gets stuck)
    if st.session_state.is_processing:
        if st.button("Reset Processing State", help="Use this if the chat is stuck in 'Processing' state"):
            st.session_state.is_processing = False
            st.rerun()

    # Quick Actions section
    st.markdown("---")
    st.subheader("Quick Actions")

    # Create columns for quick action buttons
    qa_col1, qa_col2 = st.columns(2)

    with qa_col1:
        if st.button("📝 New Python File"):
            # Set default values for Python file
            st.session_state.sandbox_filename = "new_script.py"
            st.session_state.sandbox_content = """# New Python Script

def main():
    print("Hello, SuperNova AI!")

    # Your code here

    return 0

if __name__ == "__main__":
    main()
"""
            # Switch to the Sandbox tab
            st.experimental_set_query_params(tab="Sandbox")
            st.rerun()

    with qa_col2:
        if st.button("📊 Data Analysis"):
            # Set default values for data analysis script
            st.session_state.sandbox_filename = "data_analysis.py"
            st.session_state.sandbox_content = """# Data Analysis Script

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
# data = pd.read_csv('your_data.csv')

# Create sample data
data = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'group': np.random.choice(['A', 'B', 'C'], 100)
})

# Analyze the data
print(data.head())
print(data.describe())

# Create a plot
plt.figure(figsize=(10, 6))
for group, group_data in data.groupby('group'):
    plt.scatter(group_data['x'], group_data['y'], label=group)

plt.title('Sample Data Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
"""
            # Switch to the Sandbox tab
            st.experimental_set_query_params(tab="Sandbox")
            st.rerun()

    qa_col1, qa_col2 = st.columns(2)

    with qa_col1:
        if st.button("🌐 HTML Template"):
            # Set default values for HTML file
            st.session_state.sandbox_filename = "index.html"
            st.session_state.sandbox_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SuperNova AI - Web Template</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        header {
            background-color: #2b5797;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        main {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
        }
        footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <header>
        <h1>SuperNova AI Web Template</h1>
    </header>

    <main>
        <h2>Welcome to your new web page</h2>
        <p>This is a simple HTML template to get you started.</p>

        <section>
            <h3>Features</h3>
            <ul>
                <li>Clean, responsive design</li>
                <li>Simple CSS styling</li>
                <li>Ready to customize</li>
            </ul>
        </section>
    </main>

    <footer>
        <p>Created with SuperNova AI</p>
    </footer>
</body>
</html>
"""
            # Switch to the Sandbox tab
            st.experimental_set_query_params(tab="Sandbox")
            st.rerun()

    with qa_col2:
        if st.button("📋 Markdown Doc"):
            # Set default values for Markdown file
            st.session_state.sandbox_filename = "README.md"
            st.session_state.sandbox_content = """# Project Title

## Overview
A brief description of what this project does and who it's for.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
```bash
# Clone the repository
git clone https://github.com/username/project.git

# Navigate to the project directory
cd project

# Install dependencies
pip install -r requirements.txt
```

## Usage
```python
# Example code
from project import awesome_function

result = awesome_function()
print(result)
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Thanks to SuperNova AI for assistance
"""
            # Switch to the Sandbox tab
            st.experimental_set_query_params(tab="Sandbox")
            st.rerun()

    # About section
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    **SuperNova AI** is an advanced AI automation framework that combines language models with specialized tools
    for tasks like web browsing, code execution, and file operations.

    This version uses Ollama to run models locally on your machine with enhanced web browsing capabilities.
    """)

# Load custom CSS and JavaScript if available
if CUSTOM_UI_AVAILABLE:
    try:
        # Create static directory if it doesn't exist
        os.makedirs("static", exist_ok=True)

        # Try to load CSS and JS files
        load_css_and_js()

        # Use custom header
        custom_header(
            title="SuperNova AI",
            subtitle="Advanced AI Agent with Deep Thinking Capabilities",
            icon="🌟",
            bg_color="#343541"
        )
    except Exception as e:
        st.error(f"Error loading custom UI: {str(e)}")
        # Fallback to standard header
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem; background-color: #343541; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <div style="font-size: 2.5rem; margin-right: 1rem; color: #10a37f;">🌟</div>
            <div>
                <h1 style="margin: 0; color: #ececf1; font-size: 2rem; font-weight: 600;">SuperNova AI</h1>
                <p style="margin: 0; color: #8e8ea0; font-size: 1rem;">Advanced AI Agent with Deep Thinking Capabilities</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Standard header
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem; background-color: #343541; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        <div style="font-size: 2.5rem; margin-right: 1rem; color: #10a37f;">🌟</div>
        <div>
            <h1 style="margin: 0; color: #ececf1; font-size: 2rem; font-weight: 600;">SuperNova AI</h1>
            <p style="margin: 0; color: #8e8ea0; font-size: 1rem;">Advanced AI Agent with Deep Thinking Capabilities</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Create tabs for different interfaces
tab1, tab2, tab3 = st.tabs(["Chat", "Sandbox", "Files"])

with tab1:
    # Create a two-column layout for the chat interface
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Chat")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if not st.session_state.is_processing:
            if prompt := st.chat_input("What can I help you with today?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Set processing flag
                st.session_state.is_processing = True

                # Process the query with the agent workflow
                with st.spinner("Thinking..."):
                    try:
                        # No timeout for processing
                        result = run_agent_workflow(
                            user_input=prompt,
                            debug=st.session_state.debug,
                            use_enhanced_browser=st.session_state.use_enhanced_browser,
                            thinking_mode=st.session_state.thinking_mode
                        )
                        st.session_state.workflow_result = result

                        # Extract the response
                        if result["messages"] and len(result["messages"]) > 0:
                            response = result["messages"][-1].content
                        else:
                            response = "I couldn't process your request. Please try again."

                        # Add assistant message to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})

                        # Store thinking process
                        if "thinking" in result:
                            st.session_state.thinking = result["thinking"]
                            if st.session_state.debug:
                                print(f"Thinking process stored with {len(result['thinking'].get('steps', []))} steps")
                                print(f"Links: {len(result['thinking'].get('links', []))}")
                                print(f"Files: {len(result['thinking'].get('files', []))}")
                        else:
                            st.session_state.thinking = None
                            if st.session_state.debug:
                                print("No thinking process in result")

                        # Reset processing flag
                        st.session_state.is_processing = False

                        # Display assistant message
                        with st.chat_message("assistant"):
                            st.markdown(response)
                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_message})

                        with st.chat_message("assistant"):
                            st.markdown(error_message)
                            st.error("An error occurred. You can continue chatting now.")

                        # Reset processing flag
                        st.session_state.is_processing = False
                    finally:
                        # Always reset the processing flag, no matter what happened
                        st.session_state.is_processing = False

                # Rerun to update the UI
                st.rerun()
        else:
            # Use custom loading animation if available
            if CUSTOM_UI_AVAILABLE:
                try:
                    # Show a more advanced loading animation without timeout
                    loading_animation("Processing your request... This may take a while, but there's no timeout.", type="brain", infinite=True)

                    # Add a note about the lack of timeout
                    st.markdown("""
                    <div style="margin-top: 10px; padding: 10px; background-color: #343541; border-radius: 5px; border-left: 3px solid #10a37f;">
                        <p style="margin: 0; color: #ececf1;">SuperNova AI will process your request for as long as needed without timing out.</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception:
                    # Fallback to standard info message
                    st.info("Processing your request... Please wait. There is no timeout.")
            else:
                # Standard info message
                st.info("Processing your request... Please wait. There is no timeout.")

            # Add a reset button
            if st.button("Cancel and Reset"):
                st.session_state.is_processing = False
                st.rerun()

    with col2:
        st.subheader("Agent Thinking Process")

        # Add thinking visualization if custom UI is available
        if CUSTOM_UI_AVAILABLE:
            try:
                # Add a container for the thinking visualization
                thinking_visualization("thinking-vis-container")

                # Add a progress indicator without timeout
                progress_bar("thinking-progress", 0)  # No timeout
            except Exception as e:
                if st.session_state.debug:
                    st.error(f"Error loading thinking visualization: {str(e)}")

        if st.session_state.thinking:
            thinking = st.session_state.thinking

            # Display the plan if available
            if thinking.get("plan"):
                st.markdown("### Delegation Decision")

                # Join the plan into a single string for processing
                plan_text = "\n".join(thinking.get("plan", []))

                # Check if the plan contains the structured delegation format
                if "**Reasoning:**" in plan_text:
                    # Split the plan into sections
                    sections = {}
                    current_section = "intro"
                    section_content = []

                    for line in plan_text.split("\n"):
                        if line.strip().startswith("**Reasoning:**"):
                            sections[current_section] = "\n".join(section_content)
                            current_section = "reasoning"
                            section_content = [line.replace("**Reasoning:**", "").strip()]
                        elif line.strip().startswith("**Instructions for"):
                            sections[current_section] = "\n".join(section_content)
                            current_section = "instructions"
                            section_content = [line]
                        elif line.strip().startswith("**Additional Guidance:**"):
                            sections[current_section] = "\n".join(section_content)
                            current_section = "guidance"
                            section_content = [line.replace("**Additional Guidance:**", "").strip()]
                        elif line.strip().startswith("**Delegation Note:**"):
                            sections[current_section] = "\n".join(section_content)
                            current_section = "note"
                            section_content = [line.replace("**Delegation Note:**", "").strip()]
                        else:
                            section_content.append(line)

                    # Add the last section
                    sections[current_section] = "\n".join(section_content)

                    # Display the reasoning section
                    if "reasoning" in sections:
                        st.markdown(f"""
                        <div class="delegation-reasoning">
                            <h4>Reasoning</h4>
                            <p>{sections["reasoning"]}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Display the instructions section
                    if "instructions" in sections:
                        st.markdown(f"""
                        <div class="delegation-instructions">
                            {sections["instructions"]}
                        </div>
                        """, unsafe_allow_html=True)

                    # Display the guidance section
                    if "guidance" in sections:
                        st.markdown(f"""
                        <div class="delegation-guidance">
                            <h4>Additional Guidance</h4>
                            <p>{sections["guidance"]}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Display the note section
                    if "note" in sections:
                        st.markdown(f"""
                        <div class="delegation-note">
                            <h4>Delegation Note</h4>
                            <p>{sections["note"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Display the plan in the original format
                    for step in thinking.get("plan", []):
                        st.markdown(f"""
                        <div class="plan-step">
                            {step}
                        </div>
                        """, unsafe_allow_html=True)

            # Display terminal output if available
            if thinking.get("terminal_output"):
                st.markdown("### Terminal Output")
                terminal_output = ""
                for output in thinking.get("terminal_output", []):
                    terminal_output += output.get("content", "") + "\n"

                st.code(terminal_output, language="bash")

            # Display thinking steps
            st.markdown("### Thinking Steps")
            for step in thinking.get("steps", []):
                step_type = step.get("type", "")
                step_content = step.get("content", {})
                step_time = datetime.fromtimestamp(step.get("timestamp", 0)).strftime("%H:%M:%S")

                if step_type == "thinking":
                    content_text = step_content.get("content", "")
                    if isinstance(content_text, dict) and "content" in content_text:
                        content_text = content_text["content"]

                    # Determine the thinking step type based on the content
                    thought_type = step_content.get("type", "thought")
                    step_type_name = "normal"
                    css_class = "thinking-step"

                    if thought_type == "deep_thought":
                        css_class = "deep-thinking-step"
                        step_type_name = "deep"
                    elif thought_type == "super_deep_thought":
                        css_class = "super-deep-thinking-step"
                        step_type_name = "super_deep"

                    # Use custom component if available
                    if CUSTOM_UI_AVAILABLE:
                        try:
                            thinking_step(content_text, step_time, step_type_name)
                        except Exception:
                            # Fallback to standard markdown
                            st.markdown(f"""
                            <div class="{css_class}">
                                <div class="step-time">{step_time}</div>
                                <p>{content_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Standard markdown
                        st.markdown(f"""
                        <div class="{css_class}">
                            <div class="step-time">{step_time}</div>
                            <p>{content_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                elif step_type == "terminal":
                    content_text = step_content.get("content", "")
                    if isinstance(content_text, dict) and "content" in content_text:
                        content_text = content_text["content"]
                    st.markdown(f"""
                    <div class="terminal-step">
                        <div class="step-time">{step_time}</div>
                        <pre><code>{content_text}</code></pre>
                    </div>
                    """, unsafe_allow_html=True)
                elif step_type == "planning":
                    plan_content = step_content.get("content", [])
                    if not isinstance(plan_content, list):
                        if isinstance(plan_content, dict) and "content" in plan_content:
                            plan_content = plan_content["content"]
                        else:
                            plan_content = [str(plan_content)]

                    st.markdown(f"""
                    <div class="planning-step">
                        <div class="step-time">{step_time}</div>
                        <p><strong>Plan:</strong></p>
                        <ol>
                            {"".join([f"<li>{item}</li>" for item in plan_content])}
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                elif step_type == "execution":
                    # Extract action and result, handling different formats
                    if isinstance(step_content, dict):
                        action = step_content.get("action", "")
                        result = step_content.get("result", {})
                    else:
                        action = "Execute"
                        result = step_content

                    # Format the result for display
                    result_str = ""
                    if isinstance(result, dict):
                        for key, value in result.items():
                            result_str += f"<strong>{key}:</strong> {value}<br>"
                    else:
                        result_str = str(result)

                    st.markdown(f"""
                    <div class="execution-step">
                        <div class="step-time">{step_time}</div>
                        <p><strong>Action:</strong> {action}</p>
                        <p><strong>Result:</strong><br>{result_str}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Display links
            if thinking.get("links"):
                st.markdown("### Links")
                for link in thinking.get("links", []):
                    content = link.get("content", {})
                    url = content.get("url", "")
                    title = content.get("title", url)
                    description = content.get("description", "")

                    # Use custom component if available
                    if CUSTOM_UI_AVAILABLE:
                        try:
                            link_card(url, title, description)
                        except Exception:
                            # Fallback to standard markdown
                            st.markdown(f"""
                            <div class="link-card">
                                <p><strong><a href="{url}" target="_blank">{title}</a></strong></p>
                                <p>{description}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Standard markdown
                        st.markdown(f"""
                        <div class="link-card">
                            <p><strong><a href="{url}" target="_blank">{title}</a></strong></p>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)

            # Display files
            if thinking.get("files"):
                st.markdown("### Files")
                for file in thinking.get("files", []):
                    content = file.get("content", {})
                    path = content.get("path", "")
                    description = content.get("description", "")

                    # Try to determine file type from extension
                    file_type = None
                    if path and '.' in path:
                        file_type = path.split('.')[-1]

                    # Use custom component if available
                    if CUSTOM_UI_AVAILABLE:
                        try:
                            file_card(path, description, file_type)
                        except Exception:
                            # Fallback to standard markdown
                            st.markdown(f"""
                            <div class="file-card">
                                <p><strong>{path}</strong></p>
                                <p>{description}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Standard markdown
                        st.markdown(f"""
                        <div class="file-card">
                            <p><strong>{path}</strong></p>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No thinking process to display. Ask a question to see the agent's thinking process.")

# Add the sandbox interface
with tab2:
    st.subheader("Code & Command Sandbox")

    # Create tabs for code, command, and file creation
    code_tab, command_tab, file_tab = st.tabs(["Python Code", "Shell Command", "Create File"])

    # Initialize session state for sandbox
    if "sandbox_code" not in st.session_state:
        st.session_state.sandbox_code = "# Write your Python code here\n\nprint('Hello, SuperNova AI!')\n"

    if "sandbox_command" not in st.session_state:
        st.session_state.sandbox_command = "ls -la"

    if "sandbox_filename" not in st.session_state:
        st.session_state.sandbox_filename = "example.txt"

    if "sandbox_content" not in st.session_state:
        st.session_state.sandbox_content = "This is an example file created by SuperNova AI.\n\nYou can edit this content and create the file in the sandbox environment."

    if "sandbox_result" not in st.session_state:
        st.session_state.sandbox_result = None

    # Python code tab
    with code_tab:
        st.markdown("Write Python code and execute it in a sandbox environment.")

        # Code editor
        code = st_ace(
            value=st.session_state.sandbox_code,
            language="python",
            theme="monokai",
            font_size=14,
            min_lines=10,
            max_lines=30,
            key="python_editor"
        )

        # Save code to session state
        st.session_state.sandbox_code = code

        # Execute button
        if st.button("Execute Python Code"):
            with st.spinner("Executing code..."):
                try:
                    # Run the agent workflow with a sandbox task
                    result = run_agent_workflow(
                        user_input=f"Execute this Python code in the sandbox: ```python\n{code}\n```",
                        debug=st.session_state.debug,
                        use_enhanced_browser=st.session_state.use_enhanced_browser
                    )

                    # Store the result
                    st.session_state.sandbox_result = result

                    # Display the result
                    if result["result"]:
                        st.markdown("### Result")
                        st.markdown(result["result"])
                    else:
                        st.error("No result returned from the sandbox.")
                except Exception as e:
                    st.error(f"Error executing code: {str(e)}")

    # Command tab
    with command_tab:
        st.markdown("Run shell commands in a sandbox environment.")

        # Command input
        command = st.text_input("Enter shell command:", value=st.session_state.sandbox_command)

        # Save command to session state
        st.session_state.sandbox_command = command

        # Execute button
        if st.button("Execute Command"):
            with st.spinner("Executing command..."):
                try:
                    # Run the agent workflow with a sandbox task
                    result = run_agent_workflow(
                        user_input=f"Execute this shell command in the sandbox: ```bash\n{command}\n```",
                        debug=st.session_state.debug,
                        use_enhanced_browser=st.session_state.use_enhanced_browser
                    )

                    # Store the result
                    st.session_state.sandbox_result = result

                    # Display the result
                    if result["result"]:
                        st.markdown("### Result")
                        st.markdown(result["result"])
                    else:
                        st.error("No result returned from the sandbox.")
                except Exception as e:
                    st.error(f"Error executing command: {str(e)}")

    # File creation tab
    with file_tab:
        st.markdown("Create files in the SuperNova AI environment.")

        # Get the output directory from config
        from src.config.tools import FILE_CONFIG
        output_dir = FILE_CONFIG["output_dir"]

        # Create columns for directory and filename
        col1, col2 = st.columns(2)

        with col1:
            # Directory input
            if "sandbox_directory" not in st.session_state:
                st.session_state.sandbox_directory = output_dir

            directory = st.text_input("Directory:", value=st.session_state.sandbox_directory)
            st.session_state.sandbox_directory = directory

        with col2:
            # Filename input
            filename = st.text_input("Filename:", value=st.session_state.sandbox_filename)
            st.session_state.sandbox_filename = filename

        # File type selection
        file_types = {
            "Text": ".txt",
            "Markdown": ".md",
            "Python": ".py",
            "JavaScript": ".js",
            "HTML": ".html",
            "CSS": ".css",
            "JSON": ".json",
            "YAML": ".yaml",
            "XML": ".xml",
            "CSV": ".csv",
            "Shell Script": ".sh",
            "Batch File": ".bat",
            "C/C++": ".cpp",
            "Java": ".java",
            "Go": ".go",
            "Ruby": ".rb",
            "PHP": ".php",
        }

        # Determine file type from extension or let user select
        _, file_ext = os.path.splitext(filename)
        if file_ext:
            # Find the file type from extension
            file_type_name = "Text"  # Default
            for name, ext in file_types.items():
                if ext == file_ext.lower():
                    file_type_name = name
                    break
        else:
            # Let user select file type
            file_type_name = st.selectbox("File Type:", list(file_types.keys()))

        # Determine language for editor
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".json": "json",
            ".md": "markdown",
            ".xml": "xml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".sh": "bash",
            ".bash": "bash",
            ".cpp": "c_cpp",
            ".c": "c_cpp",
            ".h": "c_cpp",
            ".hpp": "c_cpp",
            ".java": "java",
            ".go": "golang",
            ".rb": "ruby",
            ".php": "php",
        }

        # Get the extension from the selected file type
        selected_ext = file_types[file_type_name]
        editor_language = language_map.get(selected_ext, "text")

        # File content editor
        content = st_ace(
            value=st.session_state.sandbox_content,
            language=editor_language,
            theme="monokai",
            font_size=14,
            min_lines=15,
            max_lines=40,
            key="file_editor"
        )

        # Save content to session state
        st.session_state.sandbox_content = content

        # Create file button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create File with AI", help="Use SuperNova AI to create and improve the file"):
                with st.spinner("Creating file with AI..."):
                    try:
                        # Ensure filename has the correct extension
                        if not filename.endswith(selected_ext):
                            filename = filename + selected_ext

                        # Create full path
                        full_path = os.path.join(directory, filename)

                        # Run the agent workflow with a file creation task
                        result = run_agent_workflow(
                            user_input=f"Create a file named {full_path} with the following content:\n\n```{editor_language}\n{content}\n```",
                            debug=st.session_state.debug,
                            use_enhanced_browser=st.session_state.use_enhanced_browser,
                            thinking_mode=st.session_state.thinking_mode
                        )

                        # Store the result
                        st.session_state.sandbox_result = result

                        # Display the result
                        if result["result"]:
                            st.success(f"File created successfully at {full_path}")
                            st.markdown("### AI Feedback")
                            st.markdown(result["result"])
                        else:
                            st.error("No result returned from the AI.")
                    except Exception as e:
                        st.error(f"Error creating file: {str(e)}")

        with col2:
            if st.button("Save File Directly", help="Save the file directly without AI processing"):
                with st.spinner("Saving file..."):
                    try:
                        # Ensure filename has the correct extension
                        if not filename.endswith(selected_ext):
                            filename = filename + selected_ext

                        # Create directory if it doesn't exist
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        # Create full path
                        full_path = os.path.join(directory, filename)

                        # Write the file
                        with open(full_path, "w") as f:
                            f.write(content)

                        st.success(f"File saved successfully at {full_path}")
                    except Exception as e:
                        st.error(f"Error saving file: {str(e)}")

# Add the Files tab
with tab3:
    st.subheader("File Browser")

    # Add file upload component
    st.markdown("### Upload Files")
    uploaded_file = st.file_uploader("Upload a file to the output directory", type=None, accept_multiple_files=False)

    if uploaded_file is not None:
        # Get the output directory from config
        from src.config.tools import FILE_CONFIG
        output_dir = FILE_CONFIG["output_dir"]

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the uploaded file
        file_path = os.path.join(output_dir, uploaded_file.name)

        # Check if file already exists
        if os.path.exists(file_path):
            overwrite = st.checkbox("File already exists. Overwrite?")
            if not overwrite:
                st.warning(f"Upload canceled. File {uploaded_file.name} already exists.")
            else:
                # Save the file
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File {uploaded_file.name} uploaded successfully to {output_dir}!")
        else:
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully to {output_dir}!")

    st.markdown("---")

    # Get the output directory from config
    from src.config.tools import FILE_CONFIG
    output_dir = FILE_CONFIG["output_dir"]

    # Create the output directory if it doesn't exist
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List files in the output directory
    files = os.listdir(output_dir)

    if not files:
        st.info(f"No files found in the {output_dir} directory. Create files using the Sandbox tab or by asking SuperNova AI to create files for you.")
    else:
        # Display files in a table
        file_data = []
        for file in files:
            file_path = os.path.join(output_dir, file)
            file_size = os.path.getsize(file_path)
            file_modified = os.path.getmtime(file_path)
            file_data.append({
                "File": file,
                "Size": f"{file_size / 1024:.2f} KB",
                "Modified": datetime.fromtimestamp(file_modified).strftime("%Y-%m-%d %H:%M:%S"),
                "Path": file_path
            })

        # Create a dataframe for the files
        import pandas as pd
        df = pd.DataFrame(file_data)

        # Display the files table
        st.dataframe(df, use_container_width=True)

        # File viewer
        st.subheader("File Viewer")
        selected_file = st.selectbox("Select a file to view", ["Select a file..."] + files)

        if selected_file != "Select a file...":
            file_path = os.path.join(output_dir, selected_file)

            # Get file extension
            _, file_ext = os.path.splitext(selected_file)

            # Read file content
            try:
                with open(file_path, "r") as f:
                    file_content = f.read()

                # Determine language for syntax highlighting
                language = "text"
                if file_ext in [".py"]:
                    language = "python"
                elif file_ext in [".js", ".jsx"]:
                    language = "javascript"
                elif file_ext in [".ts", ".tsx"]:
                    language = "typescript"
                elif file_ext in [".html", ".htm"]:
                    language = "html"
                elif file_ext in [".css"]:
                    language = "css"
                elif file_ext in [".json"]:
                    language = "json"
                elif file_ext in [".md"]:
                    language = "markdown"
                elif file_ext in [".xml"]:
                    language = "xml"
                elif file_ext in [".yaml", ".yml"]:
                    language = "yaml"

                # Display file content with syntax highlighting
                st.code(file_content, language=language)

                # Download button
                st.download_button(
                    label="Download File",
                    data=file_content,
                    file_name=selected_file,
                    mime="text/plain"
                )

                # Delete button
                if st.button("Delete File"):
                    try:
                        os.remove(file_path)
                        st.success(f"File {selected_file} deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting file: {str(e)}")

            except UnicodeDecodeError:
                st.error("This file cannot be displayed as text. It may be a binary file.")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by SuperNova AI with Ollama | Running models locally")
