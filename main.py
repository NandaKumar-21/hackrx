from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

from document_ingestion.ingest import extract_text
from parser import query_to_json
from schema import ParsedQuery
from search_engine import find_most_relevant_chunk
from answer_generator import generate_answer

app = FastAPI()

class Submission(BaseModel):
    query: str
    file_path: str  # Absolute or relative to server root

@app.post("/api/v1/hackrx/run")
async def run_pipeline(submission: Submission):
    try:
        # 1. Extract document text
        document_text = extract_text(submission.file_path)

        # 2. Parse query into structured JSON
        raw_json = query_to_json(submission.query, document_text)

        # 3. Validate JSON
        json_dict = json.loads(raw_json)
        parsed = ParsedQuery.model_validate(json_dict)

        # 4. Build search query
        search_query = f"Information about {parsed.entity.document_section or ''} for {parsed.entity.condition or ''}"

        # 5. Chunk document and find relevant content
        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]
        best_chunks, _ = find_most_relevant_chunk(search_query, chunks)

        # 6. Generate answer
        final_answer = generate_answer(submission.query, best_chunks[0])

        return JSONResponse(content={"answer": final_answer, "success": True})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
