from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.domain.document import Document
from src.domain.chunk import Chunk


class Chunker:

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        print(f"[+] Dividiendo documentos en chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")

        all_chunks = []

        for document in documents:
            chunks = self._chunk_single_document(document)
            all_chunks.extend(chunks)

        print(f"[+] Generados {len(all_chunks)} chunks")
        return all_chunks

    def _chunk_single_document(self, document: Document) -> List[Chunk]:
        text_chunks = self.splitter.split_text(document.content)

        return [
            Chunk(
                content=chunk_text,
                source=document.source,
                chunk_id=i
            )
            for i, chunk_text in enumerate(text_chunks)
        ]
