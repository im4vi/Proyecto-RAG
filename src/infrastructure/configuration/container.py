from functools import lru_cache
from src.infrastructure.configuration.config import Config
from src.infrastructure.services.embedding_service import EmbeddingService
from src.infrastructure.services.ollama_llm_service import OllamaLLMService
from src.infrastructure.services.gemini_llm_service import GeminiLLMService
from src.infrastructure.services.pdf_loader import PDFLoader
from src.infrastructure.services.text_cleaner import TextCleaner
from src.infrastructure.services.chunker import Chunker
from src.infrastructure.repositories.document_repository import DocumentRepository
from src.infrastructure.repositories.vector_repository import VectorRepository
from src.application.use_cases.ask_question_use_case import AskQuestionUseCase
from src.application.use_cases.index_documents_use_case import IndexDocumentsUseCase
from src.application.services import LLMPort


def get_llm_service(llm_type: str = None) -> LLMPort:
    """Factory: crea el servicio LLM según el tipo especificado"""
    if llm_type is None:
        llm_type = Config.DEFAULT_LLM
    
    if llm_type == "gemini":
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no configurada en .env")
        return GeminiLLMService(
            api_key=Config.GEMINI_API_KEY,
            model=Config.GEMINI_MODEL
        )
    elif llm_type == "ollama":
        return OllamaLLMService(
            base_url=Config.OLLAMA_HOST,
            model=Config.OLLAMA_MODEL
        )
    else:
        raise ValueError(f"LLM type '{llm_type}' no soportado. Usa 'ollama' o 'gemini'")


def get_ask_question_use_case(llm_type: str = None) -> AskQuestionUseCase:
    """Dependency injection: crea el caso de uso con el LLM especificado"""
    Config.ensure_directories()
    
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )
    
    llm_service = get_llm_service(llm_type)
    
    use_case = AskQuestionUseCase(
        vector_repository=vector_repository,
        llm_service=llm_service,
        top_k=Config.TOP_K
    )
    
    return use_case


@lru_cache()
def get_index_documents_use_case() -> IndexDocumentsUseCase:
    """Dependency injection: crea el caso de uso IndexDocuments"""
    Config.ensure_directories()
    
    pdf_loader = PDFLoader()
    text_cleaner = TextCleaner()
    chunker = Chunker(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)
    
    document_repository = DocumentRepository(storage_path=Config.CLEAN_DATA_PATH)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )
    
    use_case = IndexDocumentsUseCase(
        document_loader=pdf_loader,
        text_cleaner=text_cleaner,
        chunker=chunker,
        document_repository=document_repository,
        vector_repository=vector_repository
    )
    
    return use_case
