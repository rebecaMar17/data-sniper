# 🎯 Data Sniper | AI Document Extractor

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Gemini API](https://img.shields.io/badge/Gemini_2.0-8E75B2?style=flat&logo=google)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css)

Data Sniper es una herramienta con arquitectura SaaS que utiliza Inteligencia Artificial para extraer datos estructurados de documentos no estructurados (PDFs, facturas, contratos, etc.) de forma completamente dinámica.

En lugar de depender de plantillas rígidas (OCR tradicional), el usuario define mediante lenguaje natural qué campos desea extraer, y el motor impulsado por LLM se encarga de analizar el contexto y devolver la información exacta.

---

## ✨ Características Principales

* **🧠 Extracción Dinámica:** El usuario decide qué extraer mediante un input de texto (ej. `nombre, teléfono, total_factura, IBAN`). La IA adapta su búsqueda en tiempo real.
* **📄 Soporte para PDFs Complejos:** Extrae texto de múltiples páginas, ignorando el "ruido" visual y las tablas desordenadas.
* **💻 Interfaz de Usuario Premium:** Frontend moderno con diseño a dos columnas, efecto Drag & Drop real, animaciones de carga y renderizado visual de resultados en tarjetas.
* **📊 Exportación Perfecta a Excel:** Descarga los datos extraídos en formato `.csv` (configurado específicamente con codificación UTF-8 BOM y separadores por punto y coma `;` para evitar problemas de caracteres raros en Excel en español).
* **🛡️ Manejo de Errores Inteligente:** Captura fallos de la API, límites de cuota (Rate Limits) y errores del servidor, mostrándolos de forma clara y amigable en la interfaz gráfica.

---

## 🛠️ Stack Tecnológico

**Backend:**
* [Python 3.x](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - Framework ultrarrápido para la creación de la API.
* [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para producción.
* [pdfplumber](https://github.com/jsvine/pdfplumber) - Librería para la extracción precisa de texto en PDFs.

**Motor de Inteligencia Artificial:**
* [Google Gemini API (gemini-2.0-flash)](https://ai.google.dev/) - Procesamiento de lenguaje natural y generación del JSON estructurado.

**Frontend:**
* HTML5 & Vanilla JavaScript.
* [Tailwind CSS](https://tailwindcss.com/) - Framework de utilidades para un diseño ágil y responsivo.
* [Phosphor Icons](https://phosphoricons.com/) - Iconografía limpia y moderna.

---

## 🚀 Instalación y Despliegue Local

Sigue estos pasos para arrancar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/data-sniper.git
cd data-sniper
```

### 2. Crear y activar un entorno virtual
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu API Key de Google AI Studio:
```env
GEMINI_API_KEY=tu_api_key_aqui
```
*(Nota de desarrollo: Si te encuentras en Europa y utilizas el Free Tier de Google, es posible que experimentes el error `429 RESOURCE_EXHAUSTED` / `limit: 0`. Para solucionarlo en local, utiliza una conexión VPN a EE.UU. o vincula un método de pago en Google Cloud).*

### 5. Iniciar el servidor
```bash
uvicorn app.main:app --reload
```

Abre tu navegador y entra en `http://127.0.0.1:8000`. ¡Sube un PDF y empieza a probar la extracción!

---

## 🤝 Contribuciones
Este proyecto fue creado como demostración técnica de integración de LLMs con FastApi. Las sugerencias, *issues* y *pull requests* son siempre bienvenidas para mejorar la herramienta.

---
Desarrollado por Rebeca Martín Sancho.
