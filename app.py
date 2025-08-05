import streamlit as st
from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk
from answer_generator import generate_answer
import json

st.title("LLM-Powered Intelligent Query–Retrieval System")

uploaded_file = st.file_uploader("Upload document (PDF, DOCX, EML)", type=["pdf", "docx", "eml"])
user_query = st.text_input("Ask your question:")

if uploaded_file and user_query:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    try:
        document_text = extract_text(uploaded_file.name)
        raw_json = query_to_json(user_query, document_text)
        json_dict = json.loads(raw_json)
        parsed = ParsedQuery.model_validate(json_dict)

        search_query = f"Information about {parsed.entity.document_section or ''} for {parsed.entity.condition or ''}"
        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]

        best_chunks, _ = find_most_relevant_chunk(search_query, chunks)
        final_answer = generate_answer(user_query, best_chunks[0])

        st.subheader("Final Answer:")
        st.success(final_answer)

    except Exception as e:
        st.error(f"Error: {e}")
