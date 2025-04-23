FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Create a non-root user and switch to it
RUN useradd -m -u 1000 user
USER user

# Set up the entry point
ENTRYPOINT ["streamlit", "run", "agent_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
