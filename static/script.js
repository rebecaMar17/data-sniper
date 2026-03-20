// static/script.js

// Esperamos a que el HTML cargue completamente antes de ejecutar nada
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf-file');
    const fileNameDisplay = document.getElementById('file-name');
    const form = document.getElementById('upload-form');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const jsonResult = document.getElementById('json-result');
    const downloadBtn = document.getElementById('download-btn'); // El botón de CSV

    let currentData = null;

    // 1. Mostrar el nombre del archivo seleccionado
    fileInput.addEventListener('change', (e) => {
        if(e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
        }
    });

    // 2. Enviar el PDF a tu API
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        loading.classList.remove('hidden');
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/v1/extract', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            currentData = data.data;

            jsonResult.textContent = JSON.stringify(data.data, null, 2);
            resultContainer.classList.remove('hidden');

        } catch (error) {
            alert("Error al conectar con la API: " + error.message);
        } finally {
            loading.classList.add('hidden');
        }
    });

    // 3. Descargar en formato CSV
    if(downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            if (!currentData) return;

            const headers = Object.keys(currentData).join(',');
            const values = Object.values(currentData).map(val => `"${val || ''}"`).join(',');
            
            const csvContent = `${headers}\n${values}`;
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "datos_extraidos.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
});