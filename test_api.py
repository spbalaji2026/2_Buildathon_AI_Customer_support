
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Read the OpenAI API key without displaying it
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("SUCCESS: OpenAI API key loaded")
else:
    print("ERROR: OpenAI API key not found")
