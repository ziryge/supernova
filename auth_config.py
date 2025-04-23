"""
Authentication configuration for SuperNova AI.
"""

# Set this to True to enable authentication
ENABLE_AUTH = False

# Define username and password for basic authentication
# You can add multiple users by adding more entries to the dictionary
USERS = {
    "admin": "supernova",  # Change this to a secure password!
    # "user2": "password2",
    # Add more users as needed
}

# Secret key for session management
# Generate a new one with: python -c "import secrets; print(secrets.token_hex(16))"
SECRET_KEY = "8f42a73054b1749f8f58848be5e6502c"
