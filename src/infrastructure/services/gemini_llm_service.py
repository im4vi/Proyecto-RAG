from google import genai
from src.application.services import LLMPort


class GeminiLLMService(LLMPort):
    """Adaptador: implementa LLM con Google Gemini"""
    
    def __init__(self, api_key: str, model: str):
        print(f"[+] Conectando con Gemini: {model}")
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str) -> str:
        """Genera texto usando Gemini"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
