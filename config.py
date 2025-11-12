"""
Configuration file for the Analytics Chatbot.
Put your Gemini API key in the .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Key - Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please create a .env file and add your API key.\n"
        "See .env.example for reference."
    )

