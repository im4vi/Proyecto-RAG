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

- LLM: Phi-3-mini (via Ollama)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Vector Store: ChromaDB
- Framework RAG: LangChain
- API: FastAPI

## Cómo levantarlo

### 1 - Clonar el repo
```bash
git clone https://github.com/im4vi/Proyecto-RAG.git
cd Proyecto-RAG
```

### 2 - Configurar variables de entorno
```bash
cp .env.example .env
```

### 3 - Ejecutar el script automático de preparación de entorno

La primera vez:

```bash
source install.sh
```

Después de esto simplemente:

```bash
source venv/bin/activate
```
