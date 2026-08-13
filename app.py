from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile
import os

from redactor import redact_docx


app = FastAPI(
    title="PII Redaction Tool",
    description="API for detecting and redacting PII from DOCX documents.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "PII Redaction Tool API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/redact")
async def redact_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only DOCX files are supported."
        )

    temp_dir = tempfile.mkdtemp()

    input_path = os.path.join(temp_dir, "input.docx")
    output_path = os.path.join(temp_dir, "redacted_output.docx")

    try:
        contents = await file.read()

        with open(input_path, "wb") as f:
            f.write(contents)

        redact_docx(input_path, output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="redacted_output.docx"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Redaction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )