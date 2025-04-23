"""
Modern UI components for SuperNova AI with ChatGPT-like interface.
"""

import streamlit as st
import time
import random
import html
from typing import List, Dict, Any, Optional, Union

def modern_header():
    """
    Display a modern header for SuperNova AI.
    """
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem; background-color: #202123; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        <div style="font-size: 2.5rem; margin-right: 1rem; background: linear-gradient(90deg, #10a37f, #25d195); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌟</div>
        <div>
            <h1 style="margin: 0; color: #ececf1; font-size: 2rem; font-weight: 600; background: linear-gradient(90deg, #ececf1, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SuperNova AI</h1>
            <p style="margin: 0; color: #8e8ea0; font-size: 1rem;">Advanced AI Agent with Deep Thinking Capabilities</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def typing_animation(message: str, speed: float = 0.01, delay: float = 0.5):
    """
    Display a typing animation for AI responses.
    
    Args:
        message: The message to display
        speed: The typing speed (seconds per character)
        delay: Initial delay before typing starts
    """
    # Create a placeholder for the message
    message_placeholder = st.empty()
    
    # Display the typing animation
    full_message = ""
    time.sleep(delay)  # Initial delay
    
    for char in message:
        full_message += char
        message_placeholder.markdown(full_message + "▌")
        time.sleep(speed * random.uniform(0.5, 1.5))  # Randomize typing speed slightly
    
    # Display the final message
    message_placeholder.markdown(full_message)
    
    return message_placeholder

def modern_chat_message(role: str, content: str, avatar: Optional[str] = None, typing: bool = False):
    """
    Display a modern chat message with typing animation option.
    
    Args:
        role: The role of the message sender (user or assistant)
        content: The message content
        avatar: Optional avatar image URL
        typing: Whether to show typing animation
    """
    # Define colors based on role
    if role == "user":
        bg_color = "#343541"
        border_color = "#444654"
        avatar_emoji = "👤"
    else:  # assistant
        bg_color = "#444654"
        border_color = "#10a37f"
        avatar_emoji = "🌟"
    
    # Use provided avatar or default emoji
    avatar_html = f'<img src="{avatar}" style="width: 30px; height: 30px; border-radius: 50%;">' if avatar else f'<div style="width: 30px; height: 30px; border-radius: 50%; background-color: {border_color}; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px;">{avatar_emoji}</div>'
    
    # Create message container
    st.markdown(f"""
    <div style="display: flex; margin-bottom: 1.5rem; padding: 1rem; border-radius: 0.5rem; background-color: {bg_color}; border-left: 3px solid {border_color};">
        <div style="margin-right: 1rem;">
            {avatar_html}
        </div>
        <div style="flex-grow: 1;">
            <div style="font-weight: 600; margin-bottom: 0.5rem; color: #ececf1;">{role.capitalize()}</div>
            <div class="message-content" id="message-{random.randint(10000, 99999)}">
                {"" if typing else content}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # If typing animation is enabled, use the typing animation
    if typing:
        return typing_animation(content)
    
    return None

def collapsible_thinking_panel(title: str, content: str, expanded: bool = False):
    """
    Create a collapsible panel for thinking process.
    
    Args:
        title: The panel title
        content: The panel content
        expanded: Whether the panel is expanded by default
    """
    panel_id = f"panel-{random.randint(10000, 99999)}"
    expanded_class = "expanded" if expanded else ""
    
    st.markdown(f"""
    <div class="collapsible-panel {expanded_class}" id="{panel_id}">
        <div class="panel-header" onclick="togglePanel('{panel_id}')">
            <div class="panel-title">{title}</div>
            <div class="panel-icon">▼</div>
        </div>
        <div class="panel-content">
            {content}
        </div>
    </div>
    
    <style>
    .collapsible-panel {{
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        background-color: #343541;
        overflow: hidden;
    }}
    
    .panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        background-color: #444654;
        cursor: pointer;
        user-select: none;
    }}
    
    .panel-title {{
        font-weight: 600;
        color: #ececf1;
    }}
    
    .panel-icon {{
        color: #8e8ea0;
        transition: transform 0.3s ease;
    }}
    
    .collapsible-panel.expanded .panel-icon {{
        transform: rotate(180deg);
    }}
    
    .panel-content {{
        padding: 0;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease, padding 0.3s ease;
    }}
    
    .collapsible-panel.expanded .panel-content {{
        padding: 1rem;
        max-height: 1000px;
    }}
    </style>
    
    <script>
    function togglePanel(panelId) {{
        const panel = document.getElementById(panelId);
        panel.classList.toggle('expanded');
    }}
    </script>
    """, unsafe_allow_html=True)

def thinking_step_modern(content: str, step_time: str, step_type: str = "normal"):
    """
    Display a modern thinking step with improved styling.
    
    Args:
        content: The step content
        step_time: The step timestamp
        step_type: The type of thinking step (normal, deep, super_deep)
    """
    # Determine CSS class based on step type
    if step_type == "deep":
        css_class = "deep-thinking-step"
        border_color = "#19c37d"
        bg_color = "#3a3b4b"
    elif step_type == "super_deep":
        css_class = "super-deep-thinking-step"
        border_color = "#25d195"
        bg_color = "#444654"
    else:
        css_class = "thinking-step"
        border_color = "#10a37f"
        bg_color = "#343541"
    
    st.markdown(f"""
    <div class="{css_class}" style="padding: 0.75rem 1rem; border-radius: 0.375rem; margin-bottom: 0.75rem; background-color: {bg_color}; border-left: 3px solid {border_color}; color: #ececf1; font-size: 0.95rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div class="step-time" style="color: #8e8ea0; font-size: 0.8rem; margin-bottom: 0.25rem; font-weight: 500;">{step_time}</div>
        <p style="color: #ececf1; margin: 0; line-height: 1.5;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def modern_file_card(path: str, description: str, file_type: Optional[str] = None):
    """
    Display a modern file card with improved styling.
    
    Args:
        path: The file path
        description: The file description
        file_type: The file type (extension)
    """
    # Determine icon based on file type
    icon = "📄"
    if file_type:
        file_type = file_type.lower()
        if file_type in ["py", "python"]:
            icon = "🐍"
        elif file_type in ["js", "javascript"]:
            icon = "📜"
        elif file_type in ["html", "htm"]:
            icon = "🌐"
        elif file_type in ["css"]:
            icon = "🎨"
        elif file_type in ["md", "markdown"]:
            icon = "📝"
        elif file_type in ["json", "yaml", "yml", "toml"]:
            icon = "📊"
        elif file_type in ["jpg", "jpeg", "png", "gif", "svg"]:
            icon = "🖼️"
    
    st.markdown(f"""
    <div style="padding: 0.75rem 1rem; border-radius: 0.375rem; margin-bottom: 0.75rem; background-color: #343541; border-left: 3px solid #10a37f; color: #ececf1; font-size: 0.95rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</div>
            <div style="font-weight: 600; color: #ececf1; font-family: 'Menlo', 'Monaco', 'Courier New', monospace; font-size: 0.9rem; background-color: #2d2d3a; padding: 0.2rem 0.4rem; border-radius: 0.25rem;">{html.escape(path)}</div>
        </div>
        <p style="margin: 0; color: #ececf1;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def modern_link_card(url: str, title: str, description: str):
    """
    Display a modern link card with improved styling.
    
    Args:
        url: The URL
        title: The link title
        description: The link description
    """
    st.markdown(f"""
    <div style="padding: 0.75rem 1rem; border-radius: 0.375rem; margin-bottom: 0.75rem; background-color: #343541; border-left: 3px solid #10a37f; color: #ececf1; font-size: 0.95rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-size: 1.5rem; margin-right: 0.5rem;">🔗</div>
            <a href="{url}" target="_blank" style="font-weight: 600; color: #10a37f; text-decoration: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{title}</a>
        </div>
        <p style="margin: 0; color: #ececf1;">{description}</p>
        <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #8e8ea0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{url}</div>
    </div>
    """, unsafe_allow_html=True)

def modern_code_block(code: str, language: str = "python"):
    """
    Display a modern code block with syntax highlighting.
    
    Args:
        code: The code to display
        language: The programming language
    """
    st.markdown(f"""
    <div style="margin: 1rem 0; border-radius: 0.5rem; overflow: hidden; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1rem; background-color: #2d2d3a; border-bottom: 1px solid #444654;">
            <div style="font-family: 'Menlo', 'Monaco', 'Courier New', monospace; font-size: 0.8rem; color: #8e8ea0;">{language}</div>
            <button onclick="copyCode(this)" style="background: none; border: none; color: #8e8ea0; cursor: pointer; font-size: 0.8rem; display: flex; align-items: center;">
                <span style="margin-right: 0.25rem;">📋</span> Copy
            </button>
        </div>
        <div style="padding: 1rem; background-color: #2d2d3a; overflow-x: auto;">
            <pre style="margin: 0; font-family: 'Menlo', 'Monaco', 'Courier New', monospace; font-size: 0.9rem; color: #ececf1;"><code>{html.escape(code)}</code></pre>
        </div>
    </div>
    
    <script>
    function copyCode(button) {
        const codeBlock = button.parentElement.nextElementSibling.querySelector('code');
        const text = codeBlock.innerText;
        
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.innerHTML;
            button.innerHTML = '<span style="margin-right: 0.25rem;">✅</span> Copied!';
            setTimeout(() => {
                button.innerHTML = originalText;
            }, 2000);
        });
    }
    </script>
    """, unsafe_allow_html=True)

def load_modern_css():
    """
    Load modern CSS styles for SuperNova AI.
    """
    st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #0f0f0f !important;
        color: #ececf1 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #202123 !important;
        border-right: 1px solid #444654 !important;
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
    
    /* Chat input styling */
    .stChatInput, [data-testid="stChatInput"] {
        background-color: #40414f !important;
        border-radius: 0.75rem !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.1) !important;
        color: #ececf1 !important;
        font-size: 1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #10a37f !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #0e8f6f !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #202123 !important;
        border-radius: 0.5rem !important;
        padding: 0.25rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8e8ea0 !important;
        border-radius: 0.25rem !important;
        padding: 0.5rem 1rem !important;
        margin: 0 0.25rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #343541 !important;
        color: #ffffff !important;
    }
    
    /* Code editor styling */
    .ace_editor {
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: #202123 !important;
        padding: 0.5rem !important;
        border-radius: 0.5rem !important;
    }
    
    .stRadio label {
        color: #ececf1 !important;
    }
    
    /* Checkbox */
    .stCheckbox > div > div > div {
        background-color: #202123 !important;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #40414f !important;
        color: #ececf1 !important;
        border: none !important;
        border-radius: 0.25rem !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div {
        background-color: #40414f !important;
        color: #ececf1 !important;
        border: none !important;
        border-radius: 0.25rem !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fadeIn {
        animation: fadeIn 0.3s ease forwards;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #202123;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444654;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #10a37f;
    }
    </style>
    """, unsafe_allow_html=True)

def modern_file_explorer(files: List[Dict[str, Any]]):
    """
    Display a modern file explorer.
    
    Args:
        files: List of file dictionaries with 'name', 'path', 'type', and 'size' keys
    """
    st.markdown("""
    <div style="border-radius: 0.5rem; overflow: hidden; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background-color: #202123; border-bottom: 1px solid #444654;">
            <div style="font-weight: 600; color: #ececf1;">Files</div>
            <div style="display: flex; gap: 0.5rem;">
                <button style="background: none; border: none; color: #8e8ea0; cursor: pointer; font-size: 0.9rem;">New</button>
                <button style="background: none; border: none; color: #8e8ea0; cursor: pointer; font-size: 0.9rem;">Upload</button>
            </div>
        </div>
        <div style="max-height: 300px; overflow-y: auto; background-color: #343541;">
    """, unsafe_allow_html=True)
    
    for file in files:
        # Determine icon based on file type
        icon = "📄"
        if file.get("type") == "directory":
            icon = "📁"
        elif file.get("type") in ["py", "python"]:
            icon = "🐍"
        elif file.get("type") in ["js", "javascript"]:
            icon = "📜"
        elif file.get("type") in ["html", "htm"]:
            icon = "🌐"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 0.5rem 1rem; border-bottom: 1px solid #444654; cursor: pointer; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#444654'" onmouseout="this.style.backgroundColor='transparent'">
            <div style="font-size: 1.25rem; margin-right: 0.75rem;">{icon}</div>
            <div style="flex-grow: 1;">
                <div style="font-weight: 500; color: #ececf1;">{file.get('name', '')}</div>
                <div style="font-size: 0.8rem; color: #8e8ea0;">{file.get('size', '')}</div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <button style="background: none; border: none; color: #8e8ea0; cursor: pointer; font-size: 0.8rem;">Edit</button>
                <button style="background: none; border: none; color: #8e8ea0; cursor: pointer; font-size: 0.8rem;">Delete</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

def voice_input_button():
    """
    Display a voice input button.
    """
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 1rem 0;">
        <button id="voice-input-button" style="background-color: #10a37f; color: white; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 1.5rem; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); transition: all 0.3s ease;">
            🎤
        </button>
    </div>
    
    <script>
    // This is a placeholder for voice input functionality
    // In a real implementation, you would use the Web Speech API
    document.getElementById('voice-input-button').addEventListener('click', function() {
        alert('Voice input is not implemented yet.');
    });
    </script>
    """, unsafe_allow_html=True)

def image_generation_panel():
    """
    Display an image generation panel.
    """
    st.markdown("<h3 style='color: #ececf1;'>Image Generation</h3>", unsafe_allow_html=True)
    
    # Prompt input
    prompt = st.text_area("Describe the image you want to generate:", height=100, 
                          placeholder="A futuristic city with flying cars and neon lights...")
    
    # Options
    col1, col2 = st.columns(2)
    
    with col1:
        style = st.selectbox("Style", ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Anime"])
    
    with col2:
        aspect_ratio = st.selectbox("Aspect Ratio", ["1:1 (Square)", "16:9 (Landscape)", "9:16 (Portrait)", "4:3 (Standard)"])
    
    # Generate button
    if st.button("Generate Image"):
        st.info("Image generation is not implemented yet. This is a placeholder for future functionality.")
        
        # Placeholder for generated image
        st.markdown("""
        <div style="width: 100%; height: 300px; background-color: #343541; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; margin: 1rem 0;">
            <div style="color: #8e8ea0; font-size: 1.25rem;">Image would appear here</div>
        </div>
        """, unsafe_allow_html=True)

def data_visualization_panel():
    """
    Display a data visualization panel.
    """
    st.markdown("<h3 style='color: #ececf1;'>Data Visualization</h3>", unsafe_allow_html=True)
    
    # Sample data input
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <p style="color: #ececf1;">Upload a CSV file or enter data manually:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    # Manual data entry
    st.text_area("Or enter data manually (CSV format):", height=100, 
                 placeholder="x,y,category\n1,2,A\n2,3,B\n3,4,A\n4,5,C")
    
    # Chart type selection
    chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Heatmap"])
    
    # Generate button
    if st.button("Generate Visualization"):
        st.info("Data visualization is not implemented yet. This is a placeholder for future functionality.")
        
        # Placeholder for visualization
        st.markdown("""
        <div style="width: 100%; height: 300px; background-color: #343541; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; margin: 1rem 0;">
            <div style="color: #8e8ea0; font-size: 1.25rem;">Visualization would appear here</div>
        </div>
        """, unsafe_allow_html=True)
