from src.infrastructure.configuration.config import Config
from src.infrastructure.services.embedding_service import EmbeddingService
from src.infrastructure.repositories.vector_repository import VectorRepository
from src.application.use_cases.ask_question_use_case import AskQuestionUseCase


def main():
    Config.ensure_directories()
    
    # Inicializar servicios
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )
    
    # Crear el caso de uso
    use_case = AskQuestionUseCase(
        vector_repository=vector_repository,
        ollama_host=Config.OLLAMA_HOST,
        ollama_model=Config.OLLAMA_MODEL,
        top_k=Config.TOP_K
    )
    
    # Preguntas de prueba
    questions = [
        "¿Qué es una User Story?",
        "¿Cómo me llamo?",
        "¿Qué criterios debe cumplir una historia de usuario?"
    ]
    
    for question in questions:
        result = use_case.execute(question)
        print("\n")


if __name__ == "__main__":
    main()
