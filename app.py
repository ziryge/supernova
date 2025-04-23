import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import base64
from PIL import Image
from io import BytesIO
from langchain_core.messages import HumanMessage
from src.workflow import run_agent_workflow
from src.config.env import LLMConfig, DEBUG

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="SuperNova AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #fff;
    }
    .chat-message.bot {
        background-color: #475063;
        color: #fff;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "vision_model" not in st.session_state:
    st.session_state.vision_model = None

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "use_agents" not in st.session_state:
    st.session_state.use_agents = False

if "debug" not in st.session_state:
    st.session_state.debug = DEBUG

# Sidebar
with st.sidebar:
    st.title("SuperNova AI")
    st.markdown("---")

    # Mode selection
    st.subheader("Mode")
    st.session_state.use_agents = st.checkbox("Use Agent Workflow", value=st.session_state.use_agents,
                                            help="Enable to use the full SuperNova AI agent workflow with specialized agents")

    # Model selection
    st.subheader("Model Settings")
    model_type = st.selectbox(
        "Select Model Type",
        ["Chat (llama3.2)", "Basic (llama3.1:8b)", "Vision (llama3.2-vision)"]
    )

    # Get model configuration based on selection
    if model_type == "Chat (llama3.2)":
        model_name = LLMConfig.REASONING_MODEL
        base_url = LLMConfig.REASONING_BASE_URL
    elif model_type == "Basic (llama3.1:8b)":
        model_name = LLMConfig.BASIC_MODEL
        base_url = LLMConfig.BASIC_BASE_URL
    else:  # Vision
        model_name = LLMConfig.VL_MODEL
        base_url = LLMConfig.VL_BASE_URL

    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Debug mode
    st.markdown("---")
    st.subheader("Debug Settings")
    st.session_state.debug = st.checkbox("Enable Debug Mode", value=st.session_state.debug)

    # Display current settings
    st.markdown("---")
    st.subheader("Current Settings")
    st.write(f"**Model:** {model_name}")
    st.write(f"**Base URL:** {base_url}")
    st.write(f"**Temperature:** {temperature}")
    st.write(f"**Agent Workflow:** {'Enabled' if st.session_state.use_agents else 'Disabled'}")
    st.write(f"**Debug Mode:** {'Enabled' if st.session_state.debug else 'Disabled'}")

    # Clear conversation button
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.conversation = None
        st.session_state.llm = None
        st.session_state.prompt = None
        st.session_state.vision_model = None
        st.session_state.workflow_result = None
        st.experimental_rerun()

    # About section
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    **SuperNova AI** is an advanced AI automation framework that combines language models with specialized tools
    for tasks like web browsing, code execution, and file operations.

    This version uses Ollama to run models locally on your machine with enhanced web browsing capabilities.
    """)

# Main content
st.title("SuperNova AI")

# Display agent cards if agent workflow is enabled
if st.session_state.use_agents:
    st.subheader("Agent Team")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; background-color: #fff;">
            <h3><span style="font-size: 2rem; margin-right: 0.5rem;">🧠</span> Supervisor</h3>
            <p>Coordinates the team and delegates tasks to specialists.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; background-color: #fff;">
            <h3><span style="font-size: 2rem; margin-right: 0.5rem;">🔍</span> Researcher</h3>
            <p>Gathers and analyzes information from various sources.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; background-color: #fff;">
            <h3><span style="font-size: 2rem; margin-right: 0.5rem;">💻</span> Coder</h3>
            <p>Writes, executes, and debugs Python code.</p>
        </div>

        <div style="border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; background-color: #fff;">
            <h3><span style="font-size: 2rem; margin-right: 0.5rem;">🌐</span> Browser</h3>
            <p>Navigates websites and extracts information.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; background-color: #fff;">
            <h3><span style="font-size: 2rem; margin-right: 0.5rem;">📁</span> File Manager</h3>
            <p>Handles file operations and document formatting.</p>
        </div>
        """, unsafe_allow_html=True)

# Initialize or update the model if needed
if not st.session_state.use_agents:
    if model_type.startswith("Vision"):
        # Initialize vision model
        if st.session_state.vision_model is None or st.session_state.vision_model.model != model_name:
            with st.spinner("Loading vision model..."):
                st.session_state.vision_model = ChatOpenAI(
                    model=model_name,
                    base_url=base_url,
                    api_key="not-needed-for-ollama",
                    temperature=temperature,
                )
    else:
        # Initialize chat model
        if st.session_state.conversation is None:
            with st.spinner("Loading model..."):
                llm = ChatOpenAI(
                    model=model_name,
                    base_url=base_url,
                    api_key="not-needed-for-ollama",
                    temperature=temperature,
                )

                # Create a prompt template
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful AI assistant running locally via Ollama."),
                    ("human", "{input}"),
                ])

                # Store the LLM and prompt in session state
                st.session_state.llm = llm
                st.session_state.prompt = prompt

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image"):
            st.image(message["image"], width=300)
        st.markdown(message["content"])

# Chat input
st.subheader("Conversation")

if st.session_state.use_agents:
    # Use the agent workflow
    if prompt := st.chat_input("What can I help you with today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the query with the agent workflow
        with st.spinner("Thinking..."):
            try:
                result = run_agent_workflow(user_input=prompt, debug=st.session_state.debug)
                st.session_state.workflow_result = result

                # Extract the response
                if result["messages"] and len(result["messages"]) > 0:
                    response = result["messages"][-1].content
                else:
                    response = "I couldn't process your request. Please try again."

                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Display assistant message
                with st.chat_message("assistant"):
                    st.markdown(response)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})

                with st.chat_message("assistant"):
                    st.markdown(error_message)
else:
    # Use the simple chat or vision model
    if model_type.startswith("Vision"):
        # For vision model, allow image upload
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=300)

            # Convert the image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Get user prompt
            prompt = st.text_input("Ask about the image:")

            if prompt and st.button("Send"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt, "image": image})

                # Create the message with the image
                message = HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                )

                # Get the response
                with st.spinner("Thinking..."):
                    response = st.session_state.vision_model.invoke([message])

                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.content})

                # Rerun to update the UI
                st.experimental_rerun()
    else:
        # For chat model, use standard chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    formatted_prompt = st.session_state.prompt.format_messages(input=prompt)
                    response = st.session_state.llm.invoke(formatted_prompt)
                    st.markdown(response.content)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.content})

# Display debug information if enabled
if st.session_state.debug and st.session_state.workflow_result:
    st.markdown("---")
    st.subheader("Debug Information")

    with st.expander("Workflow Details"):
        if "tasks" in st.session_state.workflow_result:
            for i, task in enumerate(st.session_state.workflow_result["tasks"], 1):
                st.markdown(f"**Task {i}:** {task.get('task', 'Unknown task')}")
                st.markdown(f"**Specialist:** {task.get('specialist', 'Unknown')}")
                st.markdown(f"**Duration:** {task.get('end_time', 0) - task.get('start_time', 0):.2f} seconds")
                st.markdown("---")

# Footer
st.markdown("---")
st.caption("Powered by SuperNova AI with Ollama | Running models locally")
