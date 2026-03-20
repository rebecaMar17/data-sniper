from fastapi import FastAPI, UploadFile, File

app = FastAPI(
    title="API Devorador de Burocracia",
    description="Extrae datos estructurados de PDFs",
    version="1.0.0"
)
@app.get("/")
def read_root():
    return {"mensaje": "El devorador de burocracia esta vivo"}

@app.post("/api/v1/extraer-factura")
async def extraer_datos(file: UploadFile = File(...)):
    return {
        "status": "success",
        "filename": file.filename,
        "mensaje": "archivo recibido correctamente. Listo para procesar"
    }