from pathlib import Path
from src.domain.entities import Document
from src.application.services import (
    DocumentLoaderPort,
    TextCleanerPort,
    ChunkerPort,
    DocumentRepositoryPort,
    VectorRepositoryPort
)


class IndexDocumentsUseCase:
    """Caso de uso: Indexar documentos en el vector store"""
    
    def __init__(
        self,
        document_loader: DocumentLoaderPort,
        text_cleaner: TextCleanerPort,
        chunker: ChunkerPort,
        document_repository: DocumentRepositoryPort,
        vector_repository: VectorRepositoryPort
    ):
        self.document_loader = document_loader
        self.text_cleaner = text_cleaner
        self.chunker = chunker
        self.document_repository = document_repository
        self.vector_repository = vector_repository
    
    def execute(self, raw_data_path: Path) -> None:
        """Ejecuta el pipeline completo de indexación"""
        print("=" * 50)
        print("INDEXACIÓN DE DOCUMENTOS")
        print("=" * 50)
        
        # Paso 1: Cargar PDFs
        documents = self.document_loader.load_from_directory(raw_data_path)
        
        if not documents:
            print("[!] No hay documentos para procesar")
            return
        
        # Paso 2: Limpiar documentos
        print("[+] Limpiando documentos...")
        cleaned_documents = [
            self.text_cleaner.clean(doc) for doc in documents
        ]
        
        # Paso 3: Guardar documentos limpios
        print("[+] Guardando documentos limpios...")
        self.document_repository.save_all(cleaned_documents)
        
        # Paso 4: Dividir en chunks
        chunks = self.chunker.chunk_documents(cleaned_documents)
        
        # Paso 5: Guardar en vector store
        self.vector_repository.save_chunks(chunks)
        
        print("=" * 50)
        print("[+] Indexación completada exitosamente")
        print(f"[+] Documentos procesados: {len(documents)}")
        print(f"[+] Chunks generados: {len(chunks)}")
        print("=" * 50)
