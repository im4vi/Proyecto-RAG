from abc import ABC, abstractmethod
from src.domain.entities import Document


class TextCleanerPort(ABC):
    """Puerto: define cómo limpiar documentos"""
    
    @abstractmethod
    def clean(self, document: Document) -> Document:
        """Limpia un documento"""
        pass
