# SuperNova AI

SuperNova AI is a powerful agent-based AI system with enhanced web browsing capabilities and deep thinking modes. It features a modern, ChatGPT-like dark theme interface with interactive visualizations of the AI's thinking process.

## Features

- **Agent-based Workflow**: Specialized agents for different tasks (Supervisor, Researcher, Coder, etc.)
- **Deep Thinking Modes**: Normal, Deep, and Super Deep thinking modes for different levels of analysis
- **Modern UI**: ChatGPT-like dark theme interface with interactive visualizations
- **Real-time Thinking Process**: Watch the AI's thinking process unfold in real-time
- **Enhanced Web Browsing**: Powerful web browsing capabilities for research
- **No Timeout**: Process requests for as long as needed without timing out
- **Web UI**: User-friendly interface with Streamlit
- **Local Inference**: Uses Ollama to run models locally
- **Vision Capabilities**: Support for image analysis
- **Multiple Models**: Configure different models for different types of tasks

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

### Web UI (Recommended)
To run the web interface with all features:
```
streamlit run app.py
```

This will open a browser window with a user-friendly interface that supports:
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
- `app.py` - Streamlit web UI for chat and vision capabilities
- `main.py` - Command-line entry point and connection test
- `.env` - Configuration file

### Source Code
- `src/agents/` - Agent implementations (Supervisor, Researcher, Coder, etc.)
- `src/config/` - Configuration modules
- `src/prompts/` - Prompt templates for agents
- `src/tools/` - Tool implementations (search, Python REPL, file operations)
- `src/workflow/` - Agent workflow coordination

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
2. Enhanced browser agent with real web browsing capabilities
3. Intuitive Streamlit UI for easier interaction
4. Configured to work with llama3 models by default
5. Transparent thinking process visualization

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
