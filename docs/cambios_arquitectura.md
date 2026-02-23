# Refactorización: Arquitectura Hexagonal

## Cambios implementados

### 1. Domain
- **Antes:** `domain/document.py`, `domain/chunk.py`
- **Después:** `domain/entities/document.py`, `domain/entities/chunk.py`
- **Razón:** Entidades agrupadas en carpetas específicas.


### 2. Application
- **Antes:** `application/indexing_service.py`, `application/rag_service.py`
- **Después:** `application/use_cases/index_documents_use_case.py`, `application/use_cases/ask_question_use_case.py`
- **Razón:** Son casos de uso, no servicios técnicos. Nombres claros. Método `answer()` - `execute()` (estándar Clean Architecture).


### 3. Configuration
- **Antes:** `src/config.py`
- **Después:** `infrastructure/configuration/config.py`
- **Razón:** Config es infraestructura (archivos .env, variables), no lógica de negocio.


### 4. Dependency Injection
- **Antes:** `infrastructure/dependencies.py`
- **Después:** `infrastructure/configuration/container.py`
- **Razón:** Nombre estándar para contenedor DI. Centraliza creación de dependencias.


### 5. API
- **Antes:** `src/api.py`
- **Después:** `infrastructure/controllers/rag_controller.py`
- **Razón:** FastAPI/HTTP es infraestructura. Controllers son adaptadores entre externo y casos de uso.


### 6. Imports actualizados
- Todos los archivos ahora importan correctamente desde nuevas ubicaciones


## Dependency Rule cumplida
```
domain (no importa de nadie)

application (solo importa domain)

infrastructure (importa domain + application)
```

**Problema anterior:** Application importaba Infrastructure directamente
**Solución:** Infrastructure inyecta dependencias a Application
