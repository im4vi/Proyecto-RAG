import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración centralizada de la aplicación"""

    # Rutas
    RAW_DATA_PATH = Path("data/raw")
    CLEAN_DATA_PATH = Path("data/clean")
    VECTORSTORE_PATH = Path(os.getenv("CHROMA_PATH", "./vectorstore"))

    # Procesamiento
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

    # Modelos
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # Vector store
    TOP_K = int(os.getenv("TOP_K", 3))

    @classmethod
    def ensure_directories(cls):
        """Crea los directorios necesarios si no existen"""
        cls.RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
        cls.CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)
        cls.VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
