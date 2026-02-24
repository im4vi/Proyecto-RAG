from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from src.domain.entities import Document


class DocumentLoaderPort(ABC):
    """Puerto: define cómo cargar documentos"""
    
    @abstractmethod
    def load_from_directory(self, directory: Path) -> List[Document]:
        """Carga documentos de un directorio"""
        pass
