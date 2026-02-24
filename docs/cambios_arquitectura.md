# Refactorización: Arquitectura Hexagonal

## Cambios implementados

### 1. Domain
- **Antes:** `domain/document.py`, `domain/chunk.py`
- **Después:** `domain/entities/document.py`, `domain/entities/chunk.py`
- **Razón:** Entidades agrupadas en carpeta específica siguiendo patrón estándar


### 2. Application - Use Cases
- **Antes:** `application/indexing_service.py`, `application/rag_service.py`
- **Después:** `application/use_cases/index_documents_use_case.py`, `application/use_cases/ask_question_use_case.py`
- **Razón:** Son casos de uso, no servicios técnicos. Nombres claros. Método `answer()` - `execute()` (estándar Clean Architecture)


### 3. Application - Ports (Interfaces)
- **Antes:** No existían
- **Después:** `application/services/` con 5 puertos:
  - `document_loader_port.py`
  - `text_cleaner_port.py`
  - `chunker_port.py`
  - `document_repository_port.py`
  - `vector_repository_port.py`
- **Razón:** Definen **contratos** que Infrastructure debe cumplir. Application solo conoce interfaces, no implementaciones concretas


### 4. Configuration
- **Antes:** `src/config.py`
- **Después:** `infrastructure/configuration/config.py`
- **Razón:** Config es infraestructura (archivos .env, variables), no lógica de negocio


### 5. Dependency Injection
- **Antes:** `infrastructure/dependencies.py`
- **Después:** `infrastructure/configuration/container.py`
- **Razón:** Nombre estándar para contenedor DI. Centraliza creación e inyección de dependencias


### 6. API
- **Antes:** `src/api.py`
- **Después:** `infrastructure/controllers/rag_controller.py`
- **Razón:** FastAPI/HTTP es infraestructura. Controllers son adaptadores entre externo y casos de uso


### 7. Infrastructure - Adapters
- **Antes:** Las clases no heredaban de nada
- **Después:** Todas las clases implementan puertos de Application:
  - `PDFLoader` implements `DocumentLoaderPort`
  - `TextCleaner` implements `TextCleanerPort`
  - `Chunker` implements `ChunkerPort`
  - `DocumentRepository` implements `DocumentRepositoryPort`
  - `VectorRepository` implements `VectorRepositoryPort`
- **Razón:** Infrastructure implementa contratos definidos en Application. Dependency Inversion Principle completo


### 8. Imports actualizados
- **Application:** Solo importa de `domain` y `application/services` (puertos)
- **Infrastructure:** Importa de `domain`, `application/services` (puertos) e implementa adaptadores
- **Razón:** Dependency Rule estrictamente cumplida

## Dependency Rule cumplida
```
domain (no importa de nadie)

application (solo importa domain)

infrastructure (importa domain + application)
```

**Problema anterior:** Application importaba Infrastructure directamente
**Solución:** Infrastructure inyecta dependencias a Application


## Retoques finales

### Ports adicionales creados
- **EmbeddingPort:** Abstrae servicio de embeddings
- **LLMPort:** Abstrae servicio de LLM con método `generate()`

### VectorRepositoryPort completo
- Método `similarity_search()` en el puerto
- No expone tipos concretos de ChromaDB

### Controller simplificado
- No duplica lógica del caso de uso
- Solo formatea respuestas

### Container completo
- Factory para `IndexDocumentsUseCase`
- Centraliza toda la creación de dependencias
