from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from src.application.use_cases.ask_question_use_case import AskQuestionUseCase
from src.infrastructure.configuration.container import get_ask_question_use_case
from src.infrastructure.configuration.config import Config

# Inicializar FastAPI
app = FastAPI(
    title="RAG Confluence API",
    description="API para consultar documentación interna usando RAG",
    version="1.0.0"
)


# Modelos de request/response
class QuestionRequest(BaseModel):
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Qué es una User Story?"
            }
        }


class ChunkInfo(BaseModel):
    content: str
    source: str
    chunk_id: int


class AnswerResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: List[ChunkInfo]


# Endpoints
@app.get("/")
def root():
    """Endpoint raíz - Info de la API"""
    return {
        "message": "RAG Confluence API",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask": "Hacer una pregunta al sistema RAG",
            "GET /health": "Verificar estado del sistema"
        }
    }


@app.get("/health")
def health_check(use_case: AskQuestionUseCase = Depends(get_ask_question_use_case)):
    """Verifica que el sistema está funcionando"""
    try:
        test_response = use_case.llm.invoke("test")
        return {
            "status": "healthy",
            "ollama": "connected",
            "model": Config.OLLAMA_MODEL,
            "vectorstore": "loaded"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"System unhealthy: {str(e)}")


@app.post("/ask", response_model=AnswerResponse)
def ask_question(
    request: QuestionRequest,
    use_case: AskQuestionUseCase = Depends(get_ask_question_use_case)
):
    """
    Hacer una pregunta al sistema RAG
    """
    try:
        # Recuperar chunks
        chunks = use_case.retrieve(request.question)
        
        # Generar respuesta
        prompt = use_case.generate_prompt(request.question, chunks)
        answer = use_case.llm.invoke(prompt)
        
        # Formatear chunks para la respuesta
        chunk_infos = [
            ChunkInfo(
                content=chunk['content'],
                source=chunk['source'],
                chunk_id=chunk['chunk_id']
            )
            for chunk in chunks
        ]
        
        return AnswerResponse(
            question=request.question,
            answer=answer,
            retrieved_chunks=chunk_infos
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
