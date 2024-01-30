from tempfile import NamedTemporaryFile
import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from generic_criteria_matcher.dependencies import get_orchestrator
import uvicorn
from devtools import debug

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate-document/")
async def evaluate_document(
    criteria_text: str = Form(None),
    document_file: UploadFile = File(...),
    orchestrator=Depends(get_orchestrator)
):

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_document_file:
        content = await document_file.read()
        temp_document_file.write(content)
        temp_document_file_path = temp_document_file.name
    
    print(criteria_text)
    try:
        return orchestrator.evaluate_document(criteria_text, temp_document_file_path)
    finally:
        # Clean up: delete the temporary file
        os.remove(temp_document_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
