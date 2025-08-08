from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from typing import List

# Assuming these are your custom modules
from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery # Make sure this import is correct
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
        # This is a potential security risk if file_path can be manipulated to access parent directories (e.g., "../...").
        # For a real application, you'd want to sanitize this input.
        file_path = os.path.join(os.path.dirname(__file__), submission.file_path)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found at: {submission.file_path}")

        # 1. Extract text from the document
        document_text = extract_text(file_path)

        # 2. Parse query and format
        # This function is the source of the `None` value.
        json_output = query_to_json(submission.query, document_text)
        
        # Validate the data against your Pydantic model.
        # The fix in `schema.py` will prevent this line from crashing.
        parsed = ParsedQuery.model_validate(json_output)

        # 3. Form search query SAFELY
        # This now handles cases where `condition` might be None.
        search_query = f"Information about {parsed.entity.document_section}"
        if parsed.entity.condition:
            search_query += f" for {parsed.entity.condition}"

        # 4. Chunk the document
        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]

        if not chunks:
            raise HTTPException(status_code=400, detail="Could not extract any content chunks from the document.")

        # 5. Retrieve best matching chunk
        best_chunks, _ = find_most_relevant_chunk(search_query, chunks)

        # 6. Generate final answer
        final_answer = generate_answer(submission.query, best_chunks[0])

        return JSONResponse(content={"answer": final_answer, "success": True})

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except Exception as e:
        # Log the full error for debugging
        print(f"An unexpected error occurred: {e}")
        # Return a generic 500 error to the client
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
