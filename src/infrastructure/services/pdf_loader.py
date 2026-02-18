from pathlib import Path
from pypdf import PdfReader
from typing import List
from src.domain.document import Document


class PDFLoader:

    def load_from_directory(self, directory: Path) -> List[Document]:
        pdf_files = list(directory.glob("*.pdf"))

        if not pdf_files:
            print(f"[!] No se encontraron archivos PDF en {directory}")
            return []

        print(f"[+] Encontrados {len(pdf_files)} archivos PDF")
        documents = []

        for pdf_path in pdf_files:
            print(f"[+] Cargando {pdf_path.name}...")
            document = self._load_single_pdf(pdf_path)
            documents.append(document)

        return documents

    def _load_single_pdf(self, file_path: Path) -> Document:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return Document.from_file(file_path, text)
