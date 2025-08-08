# answer_generator.py

import cohere
import os

# It's better practice to load keys from environment variables
# than to hardcode them directly in the script.
# co = cohere.Client(os.environ.get("COHERE_API_KEY"))
# For now, we will use the key you provided.
co = cohere.Client("korv6munGd0a3gPtoheXu3uHR6vw8xvhucrKYWae")

def generate_answer(user_query, relevant_chunk):
    """
    Generates an answer using a Cohere model based on a user query and a relevant text chunk.
    """
    prompt = f"""
Use the below document excerpt to answer the user's query clearly and concisely.

Document:
\"\"\"{relevant_chunk}\"\"\"

Question:
\"{user_query}\"

Answer:"""

    try:
        # Attempt to use the 'command-r' model first.
        response = co.generate(
            model="command-r",
            prompt=prompt,
            temperature=0.3,
            max_tokens=300
        )
        return response.generations[0].text.strip()
        
    except cohere.CohereAPIError as e:
        # If 'command-r' is not supported, print a helpful message and try a fallback model.
        print(f"Warning: Model 'command-r' failed with error: {e}")
        print("Attempting to use fallback model 'command-light'.")
        
        try:
            # Fallback to a more widely available model for debugging.
            response = co.generate(
                model="command-light",
                prompt=prompt,
                temperature=0.3,
                max_tokens=300
            )
            return response.generations[0].text.strip()
        except cohere.CohereAPIError as fallback_e:
            # If the fallback also fails, then the issue is likely the API key or connection.
            print(f"Fallback model also failed: {fallback_e}")
            raise Exception("Both primary and fallback models failed. Please check your API key and account permissions.") from fallback_e

