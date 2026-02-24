from abc import ABC, abstractmethod
from typing import List, Dict
from src.domain.entities import Chunk


class VectorRepositoryPort(ABC):
    """Puerto: define cómo persistir y buscar chunks"""
    
    @abstractmethod
    def save_chunks(self, chunks: List[Chunk]) -> None:
        """Guarda chunks en el vector store"""
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k: int) -> List[Dict]:
        """Busca chunks similares a la consulta"""
        pass
