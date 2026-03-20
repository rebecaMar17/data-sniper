from fastapi import FastAPI, UploadFile, File
from app.extractor import extract_data_from_pdf

app = FastAPI(
    title="Data Sniper API",
    description="Intelligent API to extract structured data from unstructured PDFs.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """Endpoint to check if the API is running."""
    return {"status": "ok", "message": "Data Sniper API is ready to fire 🎯"}

@app.post("/api/v1/extract")
async def extract_invoice_data(file: UploadFile = File(...)):
    """Receives a PDF file and returns extracted structured data."""
    content = await file.read()
    
    extracted_data = extract_data_from_pdf(content)
    
    return {
        "status": "success",
        "filename": file.filename,
        "data": extracted_data
    }