from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Document


class DocumentRepositoryPort(ABC):
    """Puerto: define cómo persistir documentos"""
    
    @abstractmethod
    def save_all(self, documents: List[Document]) -> None:
        """Guarda múltiples documentos"""
        pass
