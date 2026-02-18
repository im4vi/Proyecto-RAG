import re
from src.domain.document import Document


class TextCleaner:

    def clean(self, document: Document) -> Document:
        cleaned_content = self._clean_text(document.content)

        return Document(
            content=cleaned_content,
            source=document.source
        )

    def _clean_text(self, text: str) -> str:

        # Quitar URLs
        text = re.sub(r'http[s]?://\S+', '', text)

        # Quitar emails
        text = re.sub(r'\S+@\S+', '', text)

        # Quitar líneas muy cortas (headers/footers)
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) > 10]
        text = '\n'.join(lines)

        # Quitar bullets y números de lista mal formateados
        text = re.sub(r'^[\s\-\•\*\d\.]+', '', text, flags=re.MULTILINE)

        # Quitar espacios múltiples
        text = re.sub(r'\s+', ' ', text)

        # Quitar líneas vacías múltiples
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        # Quitar caracteres de control raros
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

        return text.strip()
