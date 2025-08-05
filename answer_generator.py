import cohere

co = cohere.Client("korv6munGd0a3gPtoheXu3uHR6vw8xvhucrKYWae")  # use your key

def generate_answer(user_query, relevant_chunk):
    prompt = f"""
Use the below document excerpt to answer the user's query clearly.

Document:
\"\"\"{relevant_chunk}\"\"\"

Question:
\"{user_query}\"

Answer:"""

    response = co.generate(
        model="command-r",
        prompt=prompt,
        temperature=0.3,
        max_tokens=300
    )

    return response.generations[0].text.strip()
