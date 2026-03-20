from fastapi import FastAPI, UploadFile, File
from app.extractor import extraer_texto_pdf

app = FastAPI(
    title="Data Sniper API",
    description="Extrae datos estructurados de PDFs aburridos.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensaje": "El Data Sniper está cargado y listo 🎯"}

@app.post("/api/v1/extraer-factura")
async def extraer_datos(file: UploadFile = File(...)):
    # 1. Leemos el archivo en memoria
    contenido = await file.read()
    
    # 2. Se lo pasamos a nuestro extractor inteligente (que ahora devuelve un diccionario)
    datos_extraidos = extraer_texto_pdf(contenido)
    
    # 3. Devolvemos la respuesta limpia
    return {
        "status": "success",
        "filename": file.filename,
        "datos": datos_extraidos
    }