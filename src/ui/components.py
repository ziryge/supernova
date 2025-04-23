"""
Custom UI components for SuperNova AI.
"""
import streamlit as st
import time
import random
import json
from typing import List, Dict, Any, Optional, Union, Callable

def custom_header(title: str, subtitle: str = "", icon: str = "🌟", bg_color: str = "#343541"):
    """
    Display a custom header with icon and subtitle.

    Args:
        title: The main title text
        subtitle: Optional subtitle text
        icon: Emoji or icon to display
        bg_color: Background color for the header
    """
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem; background-color: {bg_color}; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        <div style="font-size: 2.5rem; margin-right: 1rem; color: #10a37f;">{icon}</div>
        <div>
            <h1 style="margin: 0; color: #ececf1; font-size: 2rem; font-weight: 600;">{title}</h1>
            <p style="margin: 0; color: #8e8ea0; font-size: 1rem;">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def card(title: str, content: str, icon: str = None, badge: str = None, badge_color: str = "#10a37f"):
    """
    Display a card with title, content, and optional icon and badge.

    Args:
        title: Card title
        content: Card content (can include HTML)
        icon: Optional icon or emoji
        badge: Optional badge text
        badge_color: Color for the badge
    """
    icon_html = f'<span style="margin-right: 8px; font-size: 1.2em;">{icon}</span>' if icon else ''
    badge_html = f'<span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin-left: 8px;">{badge}</span>' if badge else ''

    st.markdown(f"""
    <div style="background-color: #343541; border-radius: 8px; padding: 16px; margin-bottom: 16px; border: 1px solid #2d2d3a; transition: all 0.2s ease;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="font-size: 18px; font-weight: 600; color: #ececf1; margin: 0;">{icon_html}{title}{badge_html}</h3>
        </div>
        <div style="color: #8e8ea0;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def info_card(title: str, content: str, type: str = "info"):
    """
    Display an information card with different styles based on type.

    Args:
        title: Card title
        content: Card content
        type: Card type (info, success, warning, error)
    """
    colors = {
        "info": "#3b82f6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    color = colors.get(type, colors["info"])
    icon = icons.get(type, icons["info"])

    card(title, content, icon=icon, badge=type.upper(), badge_color=color)

def loading_animation(text: str = "Processing", type: str = "spinner", infinite: bool = True):
    """
    Display a loading animation with text.

    Args:
        text: Text to display with the animation
        type: Animation type (spinner, dots, pulse, brain)
        infinite: Whether the animation should run indefinitely
    """
    animation_html = {
        "spinner": '<div class="loading-spinner"></div>',
        "dots": '<div class="loading-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
        "pulse": '<div class="loading-pulse"></div>',
        "brain": '<div class="loading-brain"></div>'
    }

    html = animation_html.get(type, animation_html["spinner"])

    # Add a pulsing effect to the text for infinite animations
    text_class = "loading-text pulse-effect" if infinite else "loading-text"

    st.markdown(f"""
    <div class="loading-container">
        {html}
        <div class="{text_class}">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def thinking_visualization(container_id: str = "thinking-vis", height: int = 150):
    """
    Create a container for the thinking visualization.

    Args:
        container_id: ID for the container
        height: Height of the visualization
    """
    st.markdown(f"""
    <div id="{container_id}" class="thinking-visualization" style="height: {height}px;"></div>
    <script>
        // This will be initialized by thinking.js when it loads
        document.addEventListener('DOMContentLoaded', function() {{
            if (typeof createThinkingVisualization === 'function') {{
                window.thinkingVis = createThinkingVisualization('{container_id}');
            }}
        }});
    </script>
    """, unsafe_allow_html=True)

def progress_bar(container_id: str = "progress-container", duration: int = 5000):
    """
    Create a progress bar container.

    Args:
        container_id: ID for the container
        duration: Duration in milliseconds for the progress bar to complete (0 for infinite)
    """
    # If duration is 0, create an infinite progress bar with animation
    if duration == 0:
        st.markdown(f"""
        <div id="{container_id}" class="progress-container">
            <div class="progress-bar-infinite"></div>
        </div>
        <style>
            .progress-bar-infinite {{
                height: 100%;
                width: 100%;
                background: linear-gradient(to right, #10a37f 30%, #343541 50%, #10a37f 70%);
                background-size: 200% 100%;
                animation: progress-animation 2s linear infinite;
            }}

            @keyframes progress-animation {{
                0% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Regular progress bar with specified duration
        st.markdown(f"""
        <div id="{container_id}" class="progress-container"></div>
        <script>
            // This will be initialized by thinking.js when it loads
            document.addEventListener('DOMContentLoaded', function() {{
                if (typeof createProgressBar === 'function') {{
                    window.progressBar = createProgressBar('{container_id}', {duration});
                    window.progressBar.start();
                }}
            }});
        </script>
        """, unsafe_allow_html=True)

def tabs_with_icons(tabs_data: List[Dict[str, str]]):
    """
    Create tabs with icons.

    Args:
        tabs_data: List of dictionaries with 'label', 'icon', and 'content' keys

    Returns:
        The selected tab index
    """
    # Create tab labels with icons
    labels = [f"{tab['icon']} {tab['label']}" for tab in tabs_data]

    # Create the tabs
    tab_index = st.tabs(labels)

    # Return the selected tab index
    return tab_index

def code_editor(code: str, language: str = "python", theme: str = "monokai", key: str = None):
    """
    Create a code editor with syntax highlighting.

    Args:
        code: Initial code content
        language: Programming language
        theme: Editor theme
        key: Unique key for the editor

    Returns:
        The edited code
    """
    try:
        from streamlit_ace import st_ace

        return st_ace(
            value=code,
            language=language,
            theme=theme,
            font_size=14,
            min_lines=10,
            max_lines=30,
            key=key or f"editor_{language}_{random.randint(1000, 9999)}"
        )
    except ImportError:
        st.warning("streamlit_ace is not installed. Using standard text area instead.")
        return st.text_area("Code Editor", value=code, height=300, key=key)

def collapsible_section(title: str, content_function: Callable, icon: str = None, default_open: bool = False):
    """
    Create a collapsible section with a title and content.

    Args:
        title: Section title
        content_function: Function that renders the content
        icon: Optional icon or emoji
        default_open: Whether the section is open by default
    """
    icon_html = f'{icon} ' if icon else ''

    is_open = st.checkbox(f"{icon_html}{title}", value=default_open)

    if is_open:
        with st.container():
            content_function()

def status_indicator(status: str, text: str = None):
    """
    Display a status indicator with text.

    Args:
        status: Status type (online, offline, busy, away)
        text: Optional text to display
    """
    colors = {
        "online": "#10b981",
        "offline": "#6b7280",
        "busy": "#ef4444",
        "away": "#f59e0b",
        "thinking": "#3b82f6"
    }

    color = colors.get(status.lower(), colors["offline"])
    display_text = text or status.capitalize()

    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="width: 10px; height: 10px; border-radius: 50%; background-color: {color}; margin-right: 8px;"></div>
        <span style="color: #8e8ea0; font-size: 14px;">{display_text}</span>
    </div>
    """, unsafe_allow_html=True)

def chat_message_enhanced(role: str, content: str, avatar: str = None, timestamp: str = None):
    """
    Display an enhanced chat message with avatar and timestamp.

    Args:
        role: Message role (user or assistant)
        content: Message content
        avatar: Avatar emoji or URL
        timestamp: Optional timestamp
    """
    is_user = role.lower() == "user"

    bg_color = "#343541" if is_user else "#444654"
    avatar_bg = "#343541" if is_user else "#10a37f"
    avatar_text = avatar or ("👤" if is_user else "🤖")

    timestamp_html = f'<div style="color: #8e8ea0; font-size: 12px; margin-top: 4px;">{timestamp}</div>' if timestamp else ''

    st.markdown(f"""
    <div style="display: flex; margin-bottom: 16px;">
        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: {avatar_bg}; display: flex; justify-content: center; align-items: center; margin-right: 12px; flex-shrink: 0;">
            {avatar_text}
        </div>
        <div style="flex-grow: 1;">
            <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; color: #ececf1;">
                {content}
            </div>
            {timestamp_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def file_card(filename: str, description: str = None, file_type: str = None, size: str = None):
    """
    Display a file card with details.

    Args:
        filename: Name of the file
        description: Optional description
        file_type: Optional file type
        size: Optional file size
    """
    # Determine file type icon
    icon = "📄"
    if file_type:
        if file_type.lower() in ["py", "python"]:
            icon = "🐍"
        elif file_type.lower() in ["js", "javascript"]:
            icon = "📜"
        elif file_type.lower() in ["html", "htm"]:
            icon = "🌐"
        elif file_type.lower() in ["css"]:
            icon = "🎨"
        elif file_type.lower() in ["md", "markdown"]:
            icon = "📝"
        elif file_type.lower() in ["json"]:
            icon = "📊"
        elif file_type.lower() in ["jpg", "jpeg", "png", "gif"]:
            icon = "🖼️"

    # Create details section
    details = []
    if file_type:
        details.append(f"<span style='color: #8e8ea0;'>Type: {file_type}</span>")
    if size:
        details.append(f"<span style='color: #8e8ea0;'>Size: {size}</span>")

    details_html = f"<div style='display: flex; gap: 12px; margin-top: 8px;'>{''.join(details)}</div>" if details else ""
    description_html = f"<p style='margin: 8px 0;'>{description}</p>" if description else ""

    st.markdown(f"""
    <div style="background-color: #343541; border-radius: 8px; padding: 12px; margin-bottom: 12px; border: 1px solid #2d2d3a;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 24px; margin-right: 12px;">{icon}</div>
            <div style="flex-grow: 1;">
                <div style="font-weight: 500; color: #ececf1;">{filename}</div>
                {description_html}
                {details_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def link_card(url: str, title: str = None, description: str = None, favicon: str = None):
    """
    Display a link card with details.

    Args:
        url: URL of the link
        title: Optional title (defaults to URL)
        description: Optional description
        favicon: Optional favicon URL
    """
    title = title or url
    favicon_html = f"<img src='{favicon}' style='width: 16px; height: 16px; margin-right: 8px;'>" if favicon else "🔗"
    description_html = f"<p style='margin: 8px 0; color: #8e8ea0;'>{description}</p>" if description else ""

    st.markdown(f"""
    <div style="background-color: #343541; border-radius: 8px; padding: 12px; margin-bottom: 12px; border: 1px solid #2d2d3a;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 16px; margin-right: 8px;">{favicon_html}</div>
            <div style="flex-grow: 1;">
                <a href="{url}" target="_blank" style="color: #10a37f; text-decoration: none; font-weight: 500;">{title}</a>
                {description_html}
                <div style="font-size: 12px; color: #6b7280; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{url}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def thinking_step(content: str, step_time: str, step_type: str = "normal"):
    """
    Display a thinking step with styling based on the type.

    Args:
        content: Step content
        step_time: Time of the step
        step_type: Type of thinking (normal, deep, super_deep)
    """
    css_class = "thinking-step"
    if step_type == "deep":
        css_class = "deep-thinking-step"
    elif step_type == "super_deep":
        css_class = "super-deep-thinking-step"

    st.markdown(f"""
    <div class="{css_class}">
        <div class="step-time">{step_time}</div>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def load_css_and_js():
    """Load custom CSS and JavaScript files."""
    import os

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(os.path.dirname(current_dir))
    # Path to static directory
    static_dir = os.path.join(project_root, "static")

    # Create static directory if it doesn't exist
    os.makedirs(static_dir, exist_ok=True)

    # Load custom CSS
    theme_css_path = os.path.join(static_dir, "theme.css")
    loading_css_path = os.path.join(static_dir, "loading.css")
    thinking_js_path = os.path.join(static_dir, "thinking.js")

    # Check if files exist and load them
    if os.path.exists(theme_css_path):
        with open(theme_css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if os.path.exists(loading_css_path):
        with open(loading_css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load custom JavaScript
    if os.path.exists(thinking_js_path):
        with open(thinking_js_path, "r") as f:
            js_content = f.read()
            st.markdown(f"<script>{js_content}</script>", unsafe_allow_html=True)
