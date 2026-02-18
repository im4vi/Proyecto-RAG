from src.config import Config
from src.infrastructure.services.pdf_loader import PDFLoader
from src.infrastructure.services.text_cleaner import TextCleaner
from src.infrastructure.services.chunker import Chunker
from src.infrastructure.services.embedding_service import EmbeddingService
from src.infrastructure.repositories.document_repository import DocumentRepository
from src.infrastructure.repositories.vector_repository import VectorRepository
from src.application.indexing_service import IndexingService


def main():
    # Asegura que existen los directorios
    Config.ensure_directories()

    # Crea servicios de infraestructura
    pdf_loader = PDFLoader()
    text_cleaner = TextCleaner()
    chunker = Chunker(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    embedding_service = EmbeddingService(model_name=Config.EMBEDDING_MODEL)

    # Crear repositorios
    document_repository = DocumentRepository(storage_path=Config.CLEAN_DATA_PATH)
    vector_repository = VectorRepository(
        storage_path=Config.VECTORSTORE_PATH,
        embedding_service=embedding_service
    )

    # Crear caso de uso
    indexing_service = IndexingService(
        pdf_loader=pdf_loader,
        text_cleaner=text_cleaner,
        chunker=chunker,
        document_repository=document_repository,
        vector_repository=vector_repository
    )

    # Ejecutar indexación
    indexing_service.index_documents(Config.RAW_DATA_PATH)


if __name__ == "__main__":
    main()
