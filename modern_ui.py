"""
SuperNova AI - Modern UI implementation with ChatGPT-like interface.
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
    from src.ui.modern_components import (
        modern_header,
        modern_chat_message,
        collapsible_thinking_panel,
        thinking_step_modern,
        modern_file_card,
        modern_link_card,
        modern_code_block,
        load_modern_css,
        modern_file_explorer,
        voice_input_button,
        image_generation_panel,
        data_visualization_panel
    )
    MODERN_UI_AVAILABLE = True
except ImportError:
    MODERN_UI_AVAILABLE = False

from src.workflow import run_agent_workflow
from src.config.env import DEBUG

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="SuperNova AI",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed",
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

# Load modern CSS
if MODERN_UI_AVAILABLE:
    load_modern_css()

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

if "current_step" not in st.session_state:
    st.session_state.current_step = None

# Always use dark theme
st.session_state.theme = "dark"

# Initialize thinking mode
from src.workflow.thinking_process import ThinkingProcess
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = ThinkingProcess.NORMAL_THINKING

# Initialize show thinking flag
if "show_thinking" not in st.session_state:
    st.session_state.show_thinking = True

# Initialize active tab
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "chat"

# Sidebar
with st.sidebar:
    st.title("SuperNova AI")
    st.markdown("---")

    # Agent Settings
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

    # Show thinking process toggle
    st.session_state.show_thinking = st.checkbox("Show Thinking Process", value=st.session_state.show_thinking,
                                        help="Toggle to show or hide the AI's thinking process")

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

    # Feature tabs
    st.markdown("---")
    st.subheader("Features")
    
    feature_tabs = ["Chat", "Code", "Files", "Images", "Data"]
    
    for tab in feature_tabs:
        if st.button(tab, key=f"tab_{tab.lower()}"):
            st.session_state.active_tab = tab.lower()
            st.rerun()

    # About section
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    **SuperNova AI** is an advanced AI automation framework that combines language models with specialized tools
    for tasks like web browsing, code execution, and file operations.

    This version uses Ollama to run models locally on your machine with enhanced web browsing capabilities.
    """)

# Display modern header
if MODERN_UI_AVAILABLE:
    modern_header()
else:
    st.title("SuperNova AI")
    st.markdown("Advanced AI Agent with Deep Thinking Capabilities")

# Main content area
if st.session_state.active_tab == "chat":
    # Chat interface
    chat_col, thinking_col = st.columns([3, 1]) if st.session_state.show_thinking else [1, 0]
    
    with chat_col:
        # Display chat messages
        for message in st.session_state.messages:
            if MODERN_UI_AVAILABLE:
                modern_chat_message(message["role"], message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input
        if not st.session_state.is_processing:
            # Voice input button (placeholder)
            if MODERN_UI_AVAILABLE:
                voice_input_button()
                
            if prompt := st.chat_input("What can I help you with today?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Display user message
                if MODERN_UI_AVAILABLE:
                    modern_chat_message("user", prompt)
                else:
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
                        else:
                            st.session_state.thinking = None

                        # Reset processing flag
                        st.session_state.is_processing = False

                        # Display assistant message
                        if MODERN_UI_AVAILABLE:
                            modern_chat_message("assistant", response, typing=True)
                        else:
                            with st.chat_message("assistant"):
                                st.markdown(response)
                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_message})

                        if MODERN_UI_AVAILABLE:
                            modern_chat_message("assistant", error_message)
                        else:
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
            st.info("Processing your request... Please wait. There is no timeout.")

            # Add a reset button
            if st.button("Cancel and Reset"):
                st.session_state.is_processing = False
                st.rerun()

    # Thinking process panel
    if st.session_state.show_thinking and thinking_col:
        with thinking_col:
            st.subheader("Thinking Process")
            
            if st.session_state.thinking:
                thinking = st.session_state.thinking
                
                # Display thinking steps
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

                        if thought_type == "deep_thought":
                            step_type_name = "deep"
                        elif thought_type == "super_deep_thought":
                            step_type_name = "super_deep"

                        # Use modern component if available
                        if MODERN_UI_AVAILABLE:
                            thinking_step_modern(content_text, step_time, step_type_name)
                        else:
                            st.text(f"{step_time}: {content_text}")
                
                # Display links
                if thinking.get("links"):
                    st.subheader("Links")
                    for link in thinking.get("links", []):
                        content = link.get("content", {})
                        url = content.get("url", "")
                        title = content.get("title", url)
                        description = content.get("description", "")

                        # Use modern component if available
                        if MODERN_UI_AVAILABLE:
                            modern_link_card(url, title, description)
                        else:
                            st.markdown(f"[{title}]({url})")
                            st.caption(description)
                
                # Display files
                if thinking.get("files"):
                    st.subheader("Files")
                    for file in thinking.get("files", []):
                        content = file.get("content", {})
                        path = content.get("path", "")
                        description = content.get("description", "")

                        # Try to determine file type from extension
                        file_type = None
                        if path and '.' in path:
                            file_type = path.split('.')[-1]

                        # Use modern component if available
                        if MODERN_UI_AVAILABLE:
                            modern_file_card(path, description, file_type)
                        else:
                            st.markdown(f"**{path}**")
                            st.caption(description)
            else:
                st.info("No thinking process to display yet. Ask a question to see the agent's thinking process.")

elif st.session_state.active_tab == "code":
    # Code interface
    st.subheader("Code Editor")
    
    # Initialize code if not in session state
    if "code_content" not in st.session_state:
        st.session_state.code_content = """# Write your Python code here

def hello_world():
    print("Hello, SuperNova AI!")
    return "Hello, World!"

if __name__ == "__main__":
    result = hello_world()
    print(f"Function returned: {result}")
"""
    
    # Code editor
    code = st_ace(
        value=st.session_state.code_content,
        language="python",
        theme="monokai",
        font_size=14,
        min_lines=20,
        max_lines=40,
        key="code_editor"
    )
    
    # Save code to session state
    st.session_state.code_content = code
    
    # Execute button
    if st.button("Execute Code"):
        with st.spinner("Executing code..."):
            try:
                # Run the agent workflow with a sandbox task
                result = run_agent_workflow(
                    user_input=f"Execute this Python code in the sandbox: ```python\n{code}\n```",
                    debug=st.session_state.debug,
                    use_enhanced_browser=st.session_state.use_enhanced_browser
                )

                # Display the result
                if result.get("result"):
                    st.subheader("Result")
                    st.code(result["result"], language="bash")
                else:
                    st.error("No result returned from the sandbox.")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

elif st.session_state.active_tab == "files":
    # Files interface
    st.subheader("File Manager")
    
    # Sample files for demonstration
    sample_files = [
        {"name": "project", "path": "/sandbox/project", "type": "directory", "size": "4.2 KB"},
        {"name": "main.py", "path": "/sandbox/main.py", "type": "py", "size": "1.2 KB"},
        {"name": "data.csv", "path": "/sandbox/data.csv", "type": "csv", "size": "2.5 KB"},
        {"name": "index.html", "path": "/sandbox/index.html", "type": "html", "size": "3.7 KB"},
        {"name": "style.css", "path": "/sandbox/style.css", "type": "css", "size": "0.8 KB"},
    ]
    
    # Display file explorer
    if MODERN_UI_AVAILABLE:
        modern_file_explorer(sample_files)
    else:
        for file in sample_files:
            st.markdown(f"**{file['name']}** ({file['size']})")
    
    # File creation form
    st.subheader("Create New File")
    
    # File path input
    file_path = st.text_input("File Path:", value="/sandbox/new_file.txt")
    
    # File content input
    file_content = st.text_area("File Content:", height=200, value="This is a new file created with SuperNova AI.")
    
    # Create file button
    if st.button("Create File"):
        with st.spinner("Creating file..."):
            try:
                # Run the agent workflow with a file creation task
                result = run_agent_workflow(
                    user_input=f"Create a file at {file_path} with the following content:\n\n{file_content}",
                    debug=st.session_state.debug,
                    use_enhanced_browser=st.session_state.use_enhanced_browser
                )

                # Display the result
                if result.get("result"):
                    st.success(f"File created successfully at {file_path}")
                else:
                    st.error("Failed to create the file.")
            except Exception as e:
                st.error(f"Error creating file: {str(e)}")

elif st.session_state.active_tab == "images":
    # Image generation interface
    if MODERN_UI_AVAILABLE:
        image_generation_panel()
    else:
        st.subheader("Image Generation")
        st.info("This feature is not available in the standard UI. Please use the modern UI.")

elif st.session_state.active_tab == "data":
    # Data visualization interface
    if MODERN_UI_AVAILABLE:
        data_visualization_panel()
    else:
        st.subheader("Data Visualization")
        st.info("This feature is not available in the standard UI. Please use the modern UI.")
