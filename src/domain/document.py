from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    content: str
    source: str

    @classmethod
    def from_file(cls, file_path: Path, content: str):
        return cls(
            content=content,
            source=file_path.name
        )
