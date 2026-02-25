import google.generativeai as genai
from src.application.services import LLMPort


class GeminiLLMService(LLMPort):
    """Adaptador: implementa LLM con Google Gemini"""
    
    def __init__(self, api_key: str, model: str):
        print(f"[+] Conectando con Gemini: {model}")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    def generate(self, prompt: str) -> str:
        """Genera texto usando Gemini"""
        response = self.model.generate_content(prompt)
        return response.text
