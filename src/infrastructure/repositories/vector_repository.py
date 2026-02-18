from pathlib import Path
from typing import List
from langchain_community.vectorstores import Chroma
from src.domain.chunk import Chunk
from src.infrastructure.services.embedding_service import EmbeddingService


class VectorRepository:

    def __init__(self, storage_path: Path, embedding_service: EmbeddingService):
        self.storage_path = storage_path
        self.embedding_service = embedding_service
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_chunks(self, chunks: List[Chunk]) -> None:
        if not chunks:
            print("[!] No hay chunks para guardar")
            return

        print(f"[+] Guardando {len(chunks)} chunks en ChromaDB...")

        # Preparar datos
        texts = [chunk.content for chunk in chunks]
        metadatas = [chunk.to_metadata() for chunk in chunks]

        # Crear vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_service.get_embedding_function(),
            metadatas=metadatas,
            persist_directory=str(self.storage_path)
        )

        print(f"[+] Vector store creado con {len(texts)} chunks")

    def load(self) -> Chroma:
        return Chroma(
            persist_directory=str(self.storage_path),
            embedding_function=self.embedding_service.get_embedding_function()
        )
