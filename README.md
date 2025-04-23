# SuperNova AI

SuperNova AI is a powerful agent-based AI system with enhanced web browsing capabilities and deep thinking modes. It features a modern, ChatGPT-like dark theme interface with interactive visualizations of the AI's thinking process, image generation, data visualization, and voice interface capabilities.

## Features

- **Agent-based Workflow**: Specialized agents for different tasks (Supervisor, Researcher, Coder, etc.)
- **Deep Thinking Modes**: Normal, Deep, and Super Deep thinking modes for different levels of analysis
- **Modern UI**: ChatGPT-like dark theme interface with interactive visualizations
- **Real-time Thinking Process**: Watch the AI's thinking process unfold in real-time
- **Enhanced Web Browsing**: Powerful web browsing capabilities for research using DuckDuckGo
- **No Timeout**: Process requests for as long as needed without timing out
- **Web UI**: User-friendly interface with Streamlit
- **Local Inference**: Uses Ollama to run models locally
- **Vision Capabilities**: Support for image analysis
- **Multiple Models**: Configure different models for different types of tasks
- **Image Generation**: Create images from text descriptions (using Stability AI or DALL-E)
- **Data Visualization**: Create interactive charts and graphs from data
- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **Code Editor**: Built-in code editor with syntax highlighting and execution
- **File Management**: Create, edit, and manage files in the sandbox environment

## Prerequisites

- Python 3.10 or higher
- Ollama installed and running (https://ollama.com/)
- Required Ollama models (already installed on your system):
  - llama3.2 (for reasoning tasks)
  - llama3.1:8b (for basic tasks)
  - llama3.2-vision (for vision tasks)

## Setup

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Ollama is running:
   ```
   ollama serve
   ```

## Running the Examples

### Modern UI (Recommended)
To run the modern ChatGPT-like interface with all features:
```
./run_modern_ui.sh
```
or
```
streamlit run modern_ui.py
```

This will open a browser window with a modern, ChatGPT-like interface that supports:
- Full agent-based workflow
- Chat with different models
- Real-time thinking process visualization
- Image generation capabilities
- Data visualization tools
- Voice interface
- Code editor with execution
- File management
- Dark theme with improved contrast

### Classic Web UI
To run the classic web interface:
```
streamlit run app.py
```

This will open a browser window with the original interface that supports:
- Full agent-based workflow (enable in sidebar)
- Chat with different models
- Vision capabilities with image upload
- Conversation memory
- Model selection and temperature adjustment
- Debug mode to see workflow details

### Creating a Test Image
To create a simple test image for the vision model:
```
python create_test_image.py
```

### Basic Test
To test the basic setup and confirm Ollama is working:
```
python main.py
```

### Simple Chat
To run a simple chat interface with memory in the terminal:
```
python simple_chat.py
```

### Interactive Agent (Experimental)
To run the interactive agent with tools:
```
python agent_fixed.py
```

The agent can (in theory):
- Search for information (simulated)
- Perform calculations
- Get the current date

Note: The agent functionality may be limited with some Ollama models.

## Configuration

Edit the `.env` file to change models or other settings. The current configuration uses:

- `llama3.2` for reasoning tasks
- `llama3.1:8b` for basic tasks
- `llama3.2-vision` for vision tasks

## Project Structure

### Main Files
- `modern_ui.py` - Modern ChatGPT-like Streamlit UI with all features
- `app.py` - Classic Streamlit web UI for chat and vision capabilities
- `main.py` - Command-line entry point and connection test
- `.env` - Configuration file
- `run_modern_ui.sh` - Script to run the modern UI

### Source Code
- `src/agents/` - Agent implementations (Supervisor, Researcher, Coder, etc.)
- `src/config/` - Configuration modules
- `src/prompts/` - Prompt templates for agents
- `src/tools/` - Tool implementations (search, Python REPL, file operations, image generation, data visualization, voice interface)
- `src/workflow/` - Agent workflow coordination
- `src/ui/` - UI components and utilities

### Utility Scripts
- `simple_chat.py` - Simple chat interface with memory
- `agent_fixed.py` - Interactive agent with tools (experimental)
- `create_test_image.py` - Script to create a test image for vision model

## Using the Agent Workflow

The agent workflow is the core feature of SuperNova AI. It uses specialized agents to handle different types of tasks:

1. **Supervisor**: Coordinates the team and delegates tasks
2. **Researcher**: Gathers and analyzes information
3. **Coder**: Writes and executes Python code
4. **File Manager**: Handles file operations

To use the agent workflow:

1. Launch the web UI: `streamlit run app.py`
2. Enable "Use Agent Workflow" in the sidebar
3. Enter your query in the chat input
4. The system will automatically delegate your task to the appropriate agent

You can enable Debug Mode to see details about which agent handled your task and how long it took.

## Advanced Usage

For more advanced usage, explore the SuperNova AI documentation and examples included in the project.

## Key Features

SuperNova AI is designed to work with Ollama for local inference, with these key features:

1. Uses Ollama for local model inference without API costs
2. Enhanced browser agent with real web browsing capabilities using DuckDuckGo
3. Modern ChatGPT-like UI with dark theme and improved contrast
4. Configured to work with llama3 models by default
5. Transparent thinking process visualization in real-time
6. Image generation capabilities (with Stability AI or DALL-E when API keys are provided)
7. Data visualization tools for creating charts and graphs
8. Voice interface for speech-to-text and text-to-speech
9. Built-in code editor with syntax highlighting and execution
10. File management system for creating and editing files

## Hosting Options

### Host on Your PC

Host SuperNova AI on your own computer so others can access it through your site. See [HOST_ON_YOUR_PC.md](HOST_ON_YOUR_PC.md) for detailed instructions.

#### Windows Quick Setup
```bash
# Run as Administrator
install_windows_service.bat
```

#### Linux Quick Setup
```bash
./install_linux_service.sh
```

#### Check Port Forwarding
```bash
python check_port_forwarding.py
```

### Cloud Deployment

Alternatively, deploy to various cloud hosting platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

#### Heroku Deployment
```bash
./deploy_heroku.sh
```

#### Docker Deployment
```bash
docker-compose up -d
```

#### Railway Deployment
Connect your GitHub repository to [Railway](https://railway.app/) for automatic deployment.

## License

SuperNova AI is provided as-is for personal and educational use.
