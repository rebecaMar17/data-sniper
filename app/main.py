from fastapi import FastAPI, UploadFile, File
from app.extractor import extraer_texto_pdf

app = FastAPI(
    title="Data Sniper API",
    description="Extrae datos estructurados de PDFs",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"mensaje": "El data sniper esta cargado y listo"}

@app.post("/api/v1/extraer-factura")
async def extraer_datos(file: UploadFile = File(...)):
    contenido = await file.read()
    texto_extraido = extraer_texto_pdf(contenido)
    return {
        "status": "success",
        "filename": file.filename,
        "texto_crudo": texto_extraido[:500] + "..."
    }