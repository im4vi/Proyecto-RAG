from pathlib import Path
from src.domain.document import Document
from src.infrastructure.services.pdf_loader import PDFLoader
from src.infrastructure.services.text_cleaner import TextCleaner
from src.infrastructure.services.chunker import Chunker
from src.infrastructure.repositories.document_repository import DocumentRepository
from src.infrastructure.repositories.vector_repository import VectorRepository


class IndexingService:

    def __init__(
        self,
        pdf_loader: PDFLoader,
        text_cleaner: TextCleaner,
        chunker: Chunker,
        document_repository: DocumentRepository,
        vector_repository: VectorRepository
    ):
        self.pdf_loader = pdf_loader
        self.text_cleaner = text_cleaner
        self.chunker = chunker
        self.document_repository = document_repository
        self.vector_repository = vector_repository

    def index_documents(self, raw_data_path: Path) -> None:
        print("=" * 50)
        print("INDEXACIÓN DE DOCUMENTOS")
        print("=" * 50)

        # Cargar PDFs
        documents = self.pdf_loader.load_from_directory(raw_data_path)

        if not documents:
            print("[!] No hay documentos para procesar")
            return

        # Limpiar documentos
        print("[+] Limpiando documentos...")
        cleaned_documents = [
            self.text_cleaner.clean(doc) for doc in documents
        ]

        # Guardar documentos limpios
        print("[+] Guardando documentos limpios...")
        self.document_repository.save_all(cleaned_documents)

        # Dividir en chunks
        chunks = self.chunker.chunk_documents(cleaned_documents)

        # Guardar en vector store
        self.vector_repository.save_chunks(chunks)

        print("=" * 50)
        print("[+] Indexación completada exitosamente")
        print(f"[+] Documentos procesados: {len(documents)}")
        print(f"[+] Chunks generados: {len(chunks)}")
        print("=" * 50)
