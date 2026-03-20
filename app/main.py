from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.extractor import extract_data_from_pdf

# 1. Creamos la aplicación (¡Esto es lo que faltaba!)
app = FastAPI(
    title="Data Sniper API",
    description="Intelligent API to extract structured data from unstructured PDFs.",
    version="1.0.0"
)

# 2. Montamos los archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Endpoint para mostrar la página web
@app.get("/")
def serve_frontend():
    """Serves the main web interface."""
    return FileResponse("static/index.html")

# 4. Endpoint de la IA dinámico
@app.post("/api/v1/extract")
async def extract_invoice_data(
    file: UploadFile = File(...), 
    fields: str = Form("name, phone, date, issuer") # Campos por defecto
):
    """Receives a PDF file and dynamic fields, returns extracted structured data."""
    content = await file.read()
    
    # Convertimos el texto separado por comas en una lista real de Python
    fields_list = [f.strip() for f in fields.split(",")]
    
    # Llamamos a nuestro extractor pasándole el PDF y lo que quiere el usuario
    extracted_data = extract_data_from_pdf(content, fields_list)
    
    return {
        "status": "success",
        "filename": file.filename,
        "data": extracted_data
    }