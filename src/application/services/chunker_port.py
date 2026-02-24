from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Document, Chunk


class ChunkerPort(ABC):
    """Puerto: define cómo dividir documentos en chunks"""
    
    @abstractmethod
    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """Divide documentos en chunks"""
        pass
