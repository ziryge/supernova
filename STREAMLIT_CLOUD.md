# Deploying SuperNova AI on Streamlit Cloud

This guide explains how to deploy SuperNova AI on Streamlit Cloud and set up the necessary API keys.

## Step 1: Push Your Code to GitHub

Make sure your code is pushed to your GitHub repository at https://github.com/ziryge/supernova.

## Step 2: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the deployment form:
   - Repository: `ziryge/supernova`
   - Branch: `main`
   - Main file path: `agent_ui.py`
   - App URL: Choose a unique subdomain (e.g., `ziryge-supernova`)

## Step 3: Add API Keys as Secrets

After creating your app, you need to add your API keys as secrets:

1. Click on the three dots next to your app in the dashboard
2. Select "Settings"
3. Go to the "Secrets" section
4. Add one or more of the following secrets (in order of preference):

```
# Choose one of these LLM providers (in order of preference):

# Option 1: Hugging Face with DeepSeek models (recommended)
HUGGINGFACE_API_KEY = "your_huggingface_api_key"

# Option 2: Groq with Llama 3 models
GROQ_API_KEY = "your_groq_api_key"

# Option 3: OpenAI
OPENAI_API_KEY = "your_openai_api_key"
```

Note: No API key is needed for web search as SuperNova AI uses DuckDuckGo, which doesn't require an API key.

You can get API keys from:
- [Hugging Face](https://huggingface.co/settings/tokens) (free account required)
- [Groq](https://console.groq.com/keys) (free account required)
- [OpenAI](https://platform.openai.com/api-keys) (credit card required)

## Step 4: Restart Your App

After adding the secrets, restart your app:

1. Click on the three dots next to your app
2. Select "Reboot app"

## How It Works

SuperNova AI is configured to automatically detect when it's running on Streamlit Cloud:

1. When running locally, it uses Ollama for language model inference
2. When running on Streamlit Cloud, it tries these providers in order:
   - Hugging Face with DeepSeek models (if HUGGINGFACE_API_KEY is provided)
   - Groq with Llama 3 models (if GROQ_API_KEY is provided)
   - OpenAI (if OPENAI_API_KEY is provided)

This hybrid approach gives you the best of both worlds:
- Local development with Ollama (free, private)
- Cloud deployment with your choice of LLM provider

## Model Selection

Depending on which API key you provide, SuperNova AI will use different models:

### Hugging Face (DeepSeek)
- For reasoning: `deepseek-ai/deepseek-coder-33b-instruct` (powerful coding model)
- For basic tasks: `deepseek-ai/deepseek-llm-7b-chat` (faster general model)

### Groq
- For reasoning: `llama3-70b-8192` (powerful general model)
- For basic tasks: `llama3-8b-8192` (faster model)

### OpenAI
- For all tasks: `gpt-3.5-turbo` (balanced model)

## Troubleshooting

If you encounter any issues:

1. Check the logs by clicking "Manage app" in the bottom right corner of your app
2. Make sure your API keys are correctly set in the Secrets section
3. Verify that your app has the necessary permissions to access your GitHub repository

## Cost Considerations

- **Hugging Face**: Free for most models, including DeepSeek models
- **Groq**: Free tier available with generous limits
- **OpenAI**: Pay-as-you-go pricing, no free tier
