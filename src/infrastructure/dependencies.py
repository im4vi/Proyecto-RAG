from functools import lru_cache
from src.config import Config
from src.infrastructure.services.embedding_service import EmbeddingService
from src.infrastructure.repositories.vector_repository import VectorRepository
from src.application.rag_service import RAGService


@lru_cache()
def get_rag_service() -> RAGService:
    """
    Crea e inyecta el RAGService.
    Se cachea para que solo se cree una vez.
    """
    Config.ensure_directories()
    
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )
    
    rag_service = RAGService(
        vector_repository=vector_repository,
        ollama_host=Config.OLLAMA_HOST,
        ollama_model=Config.OLLAMA_MODEL,
        top_k=Config.TOP_K
    )
    
    return rag_service
