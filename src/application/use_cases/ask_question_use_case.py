from typing import List, Dict
from src.application.services import VectorRepositoryPort


class AskQuestionUseCase:
    """Caso de uso: Responder preguntas usando RAG"""
    
    def __init__(
        self,
        vector_repository: VectorRepositoryPort,
        llm_service,  # Por ahora dejamos genérico
        top_k: int = 3
    ):
        self.vector_repository = vector_repository
        self.llm = llm_service
        self.top_k = top_k
        
        # Cargar el vector store
        print("[+] Cargando vector store...")
        self.vectorstore = vector_repository.load()
    
    def retrieve(self, query: str) -> List[Dict]:
        """Recupera los chunks más relevantes para una consulta"""
        print(f"[+] Buscando chunks relevantes (top-{self.top_k})...")
        
        results = self.vectorstore.similarity_search(
            query=query,
            k=self.top_k
        )
        
        retrieved_chunks = []
        for i, doc in enumerate(results):
            chunk_info = {
                'content': doc.page_content,
                'source': doc.metadata.get('source', 'unknown'),
                'chunk_id': doc.metadata.get('chunk_id', -1)
            }
            retrieved_chunks.append(chunk_info)
            print(f"  [{i+1}] {chunk_info['source']} (chunk {chunk_info['chunk_id']})")
        
        return retrieved_chunks
    
    def generate_prompt(self, query: str, chunks: List[Dict]) -> str:
        """Construye el prompt con contexto"""
        context = "\n\n".join([
            f"[Documento: {chunk['source']}]\n{chunk['content']}"
            for chunk in chunks
        ])
        
        prompt = f"""Usa el siguiente contexto de la documentación interna para responder la pregunta.
Si no encuentras la información en el contexto, dilo claramente.

CONTEXTO:
{context}

PREGUNTA: {query}

RESPUESTA:"""
        
        return prompt
    
    def execute(self, question: str) -> str:
        """
        Ejecuta el caso de uso: recibe pregunta, devuelve respuesta
        """
        print("="*50)
        print(f"PREGUNTA: {question}")
        print("="*50)
        
        # Paso 1: Recuperar chunks relevantes
        chunks = self.retrieve(question)
        
        if not chunks:
            return "No se encontró información relevante en la documentación."
        
        # Paso 2: Construir el prompt
        prompt = self.generate_prompt(question, chunks)
        
        # Paso 3: Generar respuesta
        print("[+] Generando respuesta...")
        response = self.llm.invoke(prompt)
        
        print("="*50)
        print("RESPUESTA:")
        print(response)
        print("="*50)
        
        return response
