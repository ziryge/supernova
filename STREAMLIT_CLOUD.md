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
4. Add the following secrets:

```
TAVILY_API_KEY = "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"
OPENAI_API_KEY = "your_openai_api_key"
```

You need to get an OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys).

## Step 4: Restart Your App

After adding the secrets, restart your app:

1. Click on the three dots next to your app
2. Select "Reboot app"

## How It Works

SuperNova AI is configured to automatically detect when it's running on Streamlit Cloud:

1. When running locally, it uses Ollama for language model inference
2. When running on Streamlit Cloud, it uses OpenAI's API

This hybrid approach gives you the best of both worlds:
- Local development with Ollama (free, private)
- Cloud deployment with OpenAI (reliable, accessible from anywhere)

## Troubleshooting

If you encounter any issues:

1. Check the logs by clicking "Manage app" in the bottom right corner of your app
2. Make sure your API keys are correctly set in the Secrets section
3. Verify that your app has the necessary permissions to access your GitHub repository

## Cost Considerations

Using OpenAI's API incurs costs based on usage. The app is configured to use gpt-3.5-turbo, which is relatively inexpensive. Monitor your usage on the OpenAI dashboard to avoid unexpected charges.
