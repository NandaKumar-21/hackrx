# answer_generator.py (for Google Gemini Pro)

import google.generativeai as genai
import os

# --- IMPORTANT ---
# 1. Run `pip install google-generativeai` in your terminal.
# 2. Get your free API key from https://aistudio.google.com/
# 3. Paste your API key below.
# It's even better to set it as an environment variable for security.
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

GEMINI_API_KEY = "AIzaSyDoUBWSSJwm3iSwTD5VKIG8EHB-6qDIoQk"

# This check ensures the key has been changed from the default placeholder.
if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    raise ValueError("Please paste your Gemini API key into the GEMINI_API_KEY variable.")

genai.configure(api_key=GEMINI_API_KEY)

# Configuration for the generative model
generation_config = {
  "temperature": 0.3,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 300,
}

# Safety settings to avoid harmful content
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# The model name has been updated to be more specific to fix the 404 error.
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_answer(user_query, relevant_chunk):
    """
    Generates an answer using the Gemini Pro model.
    """
    prompt = f"""
Use the below document excerpt to answer the user's query clearly and concisely.

Document:
\"\"\"{relevant_chunk}\"\"\"

Question:
\"{user_query}\"

Answer:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        raise Exception(f"Failed to generate answer from Gemini. Error: {e}")
