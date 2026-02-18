from dataclasses import dataclass


@dataclass
class Chunk:
    content: str
    source: str
    chunk_id: int

    def to_metadata(self) -> dict:
        return {
            'source': self.source,
            'chunk_id': self.chunk_id
        }
