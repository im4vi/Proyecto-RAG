from langchain_ollama import OllamaLLM
from src.application.services import LLMPort


class OllamaLLMService(LLMPort):
    """Adaptador: implementa LLM con Ollama"""
    
    def __init__(self, base_url: str, model: str):
        print(f"[+] Conectando con Ollama: {model}")
        self.llm = OllamaLLM(
            base_url=base_url,
            model=model
        )
    
    def generate(self, prompt: str) -> str:
        """Genera texto usando Ollama"""
        return self.llm.invoke(prompt)
