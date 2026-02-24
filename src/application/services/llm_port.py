from abc import ABC, abstractmethod


class LLMPort(ABC):
    """Puerto: define cómo generar texto con LLM"""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Genera texto a partir de un prompt"""
        pass
