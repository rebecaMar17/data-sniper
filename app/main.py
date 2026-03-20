from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles # NUEVO: Para servir CSS y JS
from app.extractor import extract_data_from_pdf

app = FastAPI(
    title="Data Sniper API",
    description="Intelligent API to extract structured data from unstructured PDFs.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    """Serves the main web interface."""
    return FileResponse("static/index.html")

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