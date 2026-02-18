from pathlib import Path
from typing import List
from src.domain.document import Document


class DocumentRepository:

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save(self, document: Document) -> None:
        file_path = self.storage_path / f"{Path(document.source).stem}_clean.txt"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(document.content)

        print(f"[+] Guardado en {file_path}")

    def save_all(self, documents: List[Document]) -> None:
        for document in documents:
            self.save(document)
