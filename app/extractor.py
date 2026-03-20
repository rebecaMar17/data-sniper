import pdfplumber
import io

def extraer_texto_pdf(contenido_pdf: bytes):
    texto_completo = ""

    #abrimos el PDF directamente desde los bytes en memoria
    with pdfplumber.open(io.BytesIO(contenido_pdf)) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo
