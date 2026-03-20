import pdfplumber
import io
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def extraer_texto_pdf(contenido_pdf: bytes):
    texto_completo = ""
    
    with pdfplumber.open(io.BytesIO(contenido_pdf)) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
                
    instrucciones = f"""
    Eres un experto extractor de datos. 
    A continuación te proporciono el texto extraído de un documento.
    Tu misión es extraer la siguiente información:
    - Nombre de la persona o cliente
    - Teléfono
    - Fecha del documento
    - Emisor del documento (quién lo firma o la empresa)

    Devuelve ÚNICAMENTE un JSON válido con las claves: "nombre", "telefono", "fecha", "emisor".
    Si no encuentras algún dato, pon null. No incluyas markdown (como ```json) ni texto adicional.
    
    Texto del documento:
    {texto_completo}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=instrucciones,
        )    
        texto_limpio = response.text.replace('```json', '').replace('```', '').strip()
        datos_estructurados = json.loads(texto_limpio)
        return datos_estructurados  
    except Exception as e:
        return {"error": "Fallo al procesar con IA", "detalle": str(e)}