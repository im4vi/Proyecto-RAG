# RAG Confluence - Sistema de Recuperación de Documentación Interna

Sistema RAG (Retrieval-Augmented Generation) que permite consultar 
documentación interna almacenada en Confluence mediante lenguaje natural.

## ¿Qué es este proyecto?
Sistema que permite hacer preguntas en lenguaje natural sobre documentación
interna almacenada en Confluence. 
El sistema busca los fragmentos más relevantes de la documentación y se los pasa 
a un modelo de lenguaje local (Phi-3-mini) para generar una respuesta enriquecida con contexto real.

## Requisitos previos

- Python 3.10+
- Ollama instalado y corriendo
- Modelo descargado (`ollama pull phi3:mini`)

## Stack tecnológico

- **LLM:** Phi-3-mini (ejecutado localmente via Ollama)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Vector Store:** ChromaDB
- **Framework RAG:** LangChain
- **API:** FastAPI
- **Arquitectura:** Hexagonal (puertos y adaptadores)

## Cómo levantarlo

### 1 — Clonar e instalar
```bash
git clone https://github.com/im4vi/Proyecto-RAG.git
cd Proyecto-RAG
source install.sh
```

### 2 — Indexar documentos
```bash
# Coloca PDFs de Confluence en data/raw/
cp /ruta/*.pdf data/raw/

# Indexar
python -m src.data_pipeline
```

### 3 — Arrancar API
```bash
./run_api.sh
# Abre http://localhost:8000/docs
```

---

## Ejemplos de uso

### Desde el navegador

`http://localhost:8000/docs` : Probar endpoint `POST /ask`

### Desde terminal
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué es una User Story?"}'
```

### Desde Python
```python
import requests
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "¿Cómo se valida una User Story?"}
)
print(response.json()["answer"])
```


### Pasos

1. **Crear endpoint `/validate`** que reciba User Story y devuelva si cumple criterios
2. **Desplegar como container Docker** con Ollama
3. **Comunicación HTTP** entre microservicios
4. **Añadir en producción:** autenticación, rate limiting, caching (Redis), monitoring


## Documentación adicional

- **Investigación técnica:** `docs/investigacion.md`
- **API interactiva:** http://localhost:8000/docs
