from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os

from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk
from answer_generator import generate_answer

app = FastAPI()

class Submission(BaseModel):
    query: str
    file_path: str  # relative to app folder

@app.post("/api/v1/hackrx/run")
async def run_pipeline(submission: Submission):
    try:
        # Get file path relative to where app is deployed
        file_path = os.path.join(os.path.dirname(__file__), submission.file_path)

        # Extract text from the document
        document_text = extract_text(file_path)

        # Parse query and format
        json_dict = query_to_json(submission.query, document_text)
        parsed = ParsedQuery.model_validate(json_dict)

        # Form search query
        search_query = f"Information about {parsed.entity.document_section} for {parsed.entity.condition}"

        # Chunk the document
        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]

        # Retrieve best matching chunk
        best_chunks, _ = find_most_relevant_chunk(search_query, chunks)

        # Generate final answer
        final_answer = generate_answer(submission.query, best_chunks[0])

        return JSONResponse(content={"answer": final_answer, "success": True})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
