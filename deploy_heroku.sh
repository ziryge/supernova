#!/bin/bash

# Heroku deployment script for SuperNova AI

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "You are not logged in to Heroku. Please login first."
    heroku login
fi

# Ask for app name
read -p "Enter your Heroku app name (leave blank to create a new app): " APP_NAME

if [ -z "$APP_NAME" ]; then
    # Create a new Heroku app
    echo "Creating a new Heroku app..."
    heroku create
    APP_NAME=$(heroku apps:info | grep "=== " | cut -d' ' -f2)
else
    # Check if app exists
    if ! heroku apps:info --app "$APP_NAME" &> /dev/null; then
        echo "App $APP_NAME does not exist. Creating it..."
        heroku create "$APP_NAME"
    fi
fi

echo "Deploying to Heroku app: $APP_NAME"

# Set up environment variables
echo "Setting up environment variables..."
read -p "Enter your Tavily API key (leave blank to skip): " TAVILY_API_KEY
if [ ! -z "$TAVILY_API_KEY" ]; then
    heroku config:set TAVILY_API_KEY="$TAVILY_API_KEY" --app "$APP_NAME"
fi

# Add Heroku remote if it doesn't exist
if ! git remote | grep heroku &> /dev/null; then
    git remote add heroku "https://git.heroku.com/$APP_NAME.git"
fi

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku main

# Open the app in browser
echo "Opening the app in browser..."
heroku open --app "$APP_NAME"

echo "Deployment complete!"
