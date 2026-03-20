document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('pdf-file');
    const fileNameDisplay = document.getElementById('file-name');
    const form = document.getElementById('upload-form');
    const dropZone = document.getElementById('drop-zone');
    const submitBtn = document.getElementById('submit-btn');
    
    // Paneles de la derecha
    const initialState = document.getElementById('initial-state');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const dataCards = document.getElementById('data-cards');
    const downloadBtn = document.getElementById('download-btn');

    let currentData = null;

    // --- MAGIA DEL DRAG & DROP ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    // Manejar archivo seleccionado o soltado
    fileInput.addEventListener('change', handleFile);
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files; 
        handleFile();
    });

    function handleFile() {
        if(fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
            fileNameDisplay.classList.remove('hidden');
        }
    }

    // --- ENVIAR DATOS A LA API ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        
        const file = fileInput.files[0];
        if (!file) return;

        // NUEVO: Capturamos los campos personalizados que ha escrito el usuario
        const customFieldsInput = document.getElementById('custom-fields');
        // Si el elemento no existe (porque no has actualizado el HTML aún), usamos unos por defecto
        const fields = customFieldsInput ? customFieldsInput.value : "name, phone, date, issuer";

        const formData = new FormData();
        formData.append('file', file);
        formData.append('fields', fields); // NUEVO: Enviamos los campos al backend

        // Cambios de UI al cargar
        initialState.classList.add('hidden');
        resultContainer.classList.add('hidden');
        loading.classList.remove('hidden');
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/v1/extract', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            // Si la API devuelve un error (ej. Gemini falla), lo mostramos
            if (data.data && data.data.error) {
                 throw new Error(data.data.error);
            }

            currentData = data.data;

            renderDataCards(currentData);
            
            loading.classList.add('hidden');
            resultContainer.classList.remove('hidden');

        } catch (error) {
            alert("Error al extraer datos: " + error.message);
            loading.classList.add('hidden');
            initialState.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
        }
    });

    // --- RENDERIZAR RESULTADOS VISUALES ---
    function renderDataCards(data) {
        dataCards.innerHTML = ''; // Limpiar anteriores
        
        // Mapeo de iconos básico (los campos nuevos usarán el icono 'ph-info' por defecto)
        const icons = {
            'name': 'ph-user',
            'phone': 'ph-phone',
            'date': 'ph-calendar-blank',
            'issuer': 'ph-buildings',
            'total': 'ph-currency-eur',
            'impuestos': 'ph-receipt'
        };

        for (const [key, value] of Object.entries(data)) {
            // Limpiamos la clave (quitamos espacios extra)
            const cleanKey = key.trim();
            const iconClass = icons[cleanKey.toLowerCase()] || 'ph-info';
            
            // Si es un objeto o array (como una lista de productos), lo convertimos a string legible
            let displayValue = value;
            if (typeof value === 'object' && value !== null) {
                 displayValue = JSON.stringify(value, null, 2);
            } else if (!value) {
                 displayValue = '<span class="text-slate-300 italic">No encontrado</span>';
            }

            const card = `
                <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm flex items-center gap-4">
                    <div class="bg-indigo-50 p-3 rounded-lg text-indigo-600">
                        <i class="ph ${iconClass} text-xl"></i>
                    </div>
                    <div class="overflow-hidden">
                        <p class="text-xs font-bold text-slate-400 uppercase truncate">${cleanKey}</p>
                        <pre class="text-slate-800 font-medium whitespace-pre-wrap text-sm font-sans">${displayValue}</pre>
                    </div>
                </div>
            `;
            dataCards.innerHTML += card;
        }
    }

    // --- DESCARGAR CSV ---
    if(downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            if (!currentData) return;

            const headers = Object.keys(currentData).join(';');
            
            // Mapeamos los valores. Si es un objeto, lo stringificamos para que no salga [object Object] en el CSV
            const values = Object.values(currentData).map(val => {
                if (typeof val === 'object' && val !== null) {
                    return `"${JSON.stringify(val).replace(/"/g, '""')}"`; // Escapamos comillas dobles para CSV
                }
                return `"${val || ''}"`;
            }).join(';');
            
            const csvContent = "\uFEFF" + `${headers}\n${values}`;
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