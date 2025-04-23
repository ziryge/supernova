# SuperNova AI Deployment Guide

This guide provides instructions for deploying SuperNova AI to various hosting platforms.

## Prerequisites

- Git repository with your SuperNova AI code
- Account on the hosting platform of your choice

## Option 1: Streamlit Cloud (Easiest)

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and the `agent_ui.py` file
6. Click "Deploy"

## Option 2: Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:
   ```
   heroku login
   ```
3. Create a new Heroku app:
   ```
   heroku create supernova-ai
   ```
4. Push your code to Heroku:
   ```
   git push heroku main
   ```
5. Set up environment variables:
   ```
   heroku config:set TAVILY_API_KEY=your_api_key
   ```
6. Open your app:
   ```
   heroku open
   ```

## Option 3: Railway

1. Create an account on [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Create a new project from your repository
4. Add environment variables in the Railway dashboard
5. Railway will automatically deploy your app

## Option 4: DigitalOcean App Platform

1. Create an account on [DigitalOcean](https://www.digitalocean.com/)
2. Go to the App Platform
3. Connect your GitHub repository
4. Select your repository and branch
5. Configure your app (select Python app)
6. Add environment variables
7. Deploy your app

## Option 5: AWS Elastic Beanstalk

1. Install the [AWS CLI](https://aws.amazon.com/cli/) and [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
2. Initialize your EB application:
   ```
   eb init
   ```
3. Create an environment:
   ```
   eb create supernova-ai-env
   ```
4. Deploy your application:
   ```
   eb deploy
   ```

## Environment Variables

Make sure to set these environment variables on your hosting platform:

- `TAVILY_API_KEY`: Your Tavily API key for web search
- Any other API keys or configuration variables your app needs

## Troubleshooting

- **Application Error**: Check the logs on your hosting platform
- **Dependencies Not Installing**: Make sure all dependencies are in `requirements.txt`
- **Port Issues**: Most platforms will set the `PORT` environment variable, which is used in the Procfile

## Maintenance

- Set up automatic deployments from your GitHub repository
- Monitor your application's performance and logs
- Set up alerts for any issues
