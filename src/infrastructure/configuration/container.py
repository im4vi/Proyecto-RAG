from functools import lru_cache
from src.infrastructure.configuration.config import Config
from src.infrastructure.services.embedding_service import EmbeddingService
from src.infrastructure.services.ollama_llm_service import OllamaLLMService
from src.infrastructure.repositories.vector_repository import VectorRepository
from src.application.use_cases.ask_question_use_case import AskQuestionUseCase


@lru_cache()
def get_ask_question_use_case() -> AskQuestionUseCase:
    """Dependency injection: crea e inyecta el caso de uso AskQuestion"""
    Config.ensure_directories()
    
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )
    
    llm_service = OllamaLLMService(
        base_url=Config.OLLAMA_HOST,
        model=Config.OLLAMA_MODEL
    )
    
    use_case = AskQuestionUseCase(
        vector_repository=vector_repository,
        llm_service=llm_service,
        top_k=Config.TOP_K
    )
    
    return use_case
