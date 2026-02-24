from pathlib import Path
from typing import List, Dict
from langchain_community.vectorstores import Chroma
from src.domain.entities import Chunk
from src.application.services import VectorRepositoryPort, EmbeddingPort


class VectorRepository(VectorRepositoryPort):
    """Adaptador: implementa persistencia en ChromaDB"""
    
    def __init__(self, storage_path: Path, embedding_service: EmbeddingPort):
        self.storage_path = storage_path
        self.embedding_service = embedding_service
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.vectorstore = None
    
    def save_chunks(self, chunks: List[Chunk]) -> None:
        if not chunks:
            print("[!] No hay chunks para guardar")
            return
        
        print(f"[+] Guardando {len(chunks)} chunks en ChromaDB...")
        
        texts = [chunk.content for chunk in chunks]
        metadatas = [chunk.to_metadata() for chunk in chunks]
        
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_service.get_embedding_function(),
            metadatas=metadatas,
            persist_directory=str(self.storage_path)
        )
        
        print(f"[+] Vector store creado con {len(texts)} chunks")
    
    def load(self):
        """Carga el vector store - solo para uso interno"""
        if not self.vectorstore:
            self.vectorstore = Chroma(
                persist_directory=str(self.storage_path),
                embedding_function=self.embedding_service.get_embedding_function()
            )
        return self
    
    def similarity_search(self, query: str, k: int) -> List[Dict]:
        """Busca chunks similares"""
        if not self.vectorstore:
            self.load()
        
        results = self.vectorstore.similarity_search(query=query, k=k)
        
        return [
            {
                'content': doc.page_content,
                'source': doc.metadata.get('source', 'unknown'),
                'chunk_id': doc.metadata.get('chunk_id', -1)
            }
            for doc in results
        ]
