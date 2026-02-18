from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    """Representa un documento en el dominio"""
    content: str
    source: str

    @classmethod
    def from_file(cls, file_path: Path, content: str):
        """Crea un documento desde un archivo"""
        return cls(
            content=content,
            source=file_path.name
        )
