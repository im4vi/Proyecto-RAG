from dataclasses import dataclass


@dataclass
class Chunk:
    """Representa un fragmento de documento"""
    content: str
    source: str
    chunk_id: int

    def to_metadata(self) -> dict:
        """Convierte a metadatos para el vector store"""
        return {
            'source': self.source,
            'chunk_id': self.chunk_id
        }
