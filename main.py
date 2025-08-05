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
    file_path: str  # absolute or relative to where server runs

@app.post("/api/v1/hackrx/run")
async def run_pipeline(submission: Submission):
    try:
        document_text = extract_text(submission.file_path)

        raw_json = query_to_json(submission.query, document_text)
        json_dict = json.loads(raw_json)
        parsed = ParsedQuery.model_validate(json_dict)

        search_query = f"Information about {parsed.entity.document_section} for {parsed.entity.condition}"

        lines = [line.strip() for line in document_text.split('\n') if len(line.strip()) > 30]
        chunks = [' '.join(lines[i:i+3]) for i in range(0, len(lines), 3)]
        best_chunks, _ = find_most_relevant_chunk(search_query, chunks)

        final_answer = generate_answer(submission.query, best_chunks[0])

        return JSONResponse(content={"answer": final_answer, "success": True})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
