from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    """Puerto: define cómo generar embeddings"""
    
    @abstractmethod
    def get_embedding_function(self):
        """Devuelve la función de embeddings"""
        pass
