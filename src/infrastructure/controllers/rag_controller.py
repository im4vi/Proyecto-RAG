from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from src.application.use_cases.ask_question_use_case import AskQuestionUseCase
from src.infrastructure.configuration.container import get_ask_question_use_case
from src.infrastructure.configuration.config import Config

# Inicializar FastAPI
app = FastAPI(
    title="RAG Confluence API",
    description="API para consultar documentación interna usando RAG",
    version="1.0.0"
)

# Añadir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de request/response
class QuestionRequest(BaseModel):
    question: str
    llm_type: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Qué es una User Story?",
                "llm_type": "ollama"
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
    llm_used: str

# Endpoints
@app.get("/")
def root():
    return {
        "message": "RAG Confluence API",
        "version": "1.0.0",
        "available_llms": ["ollama", "gemini"],
        "default_llm": Config.DEFAULT_LLM,
        "endpoints": {
            "POST /ask": "Hacer una pregunta al sistema RAG",
            "GET /health": "Verificar estado del sistema"
        }
    }

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy",
            "available_llms": ["ollama", "gemini"],
            "default_llm": Config.DEFAULT_LLM
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"System unhealthy: {str(e)}")


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """Hacer una pregunta al sistema RAG"""
    try:
        # Crear caso de uso con el LLM elegido
        llm_type = request.llm_type or Config.DEFAULT_LLM
        use_case = get_ask_question_use_case(llm_type)
        
        # Ejecutar
        result = use_case.execute(request.question)
        
        # Formatear respuesta
        chunk_infos = [
            ChunkInfo(
                content=chunk['content'],
                source=chunk['source'],
                chunk_id=chunk['chunk_id']
            )
            for chunk in result['chunks']
        ]
        
        return AnswerResponse(
            question=request.question,
            answer=result['answer'],
            retrieved_chunks=chunk_infos,
            llm_used=llm_type
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()  # ← AÑADE ESTA LÍNEA
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
