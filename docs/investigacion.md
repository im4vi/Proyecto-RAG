## 1 - Qué es RAG

Un RAG es un sistema donde la IA no responde solo con lo que ya sabe, sino que consulta documentos externos 
en el momento de la pregunta y usa esos datos para construir la respuesta.

No es un tipo diferente de modelo como tal, sino una forma de usar un modelo de lenguaje 
(como los que desarrolla OpenAI) junto con un sistema de búsqueda de documentos.

Las siglas significan **Retrieval-Augmented Generation**:

- **Retrieval** : recuperar documentos relevantes
- **Augmented** : enriquecer la pregunta con ese contexto
- **Generation** : el LLM genera la respuesta final

## 2 - Partes de un sistema RAG

Un RAG tiene 2 fases bien diferenciadas:

**Fase de indexación** (1 vez, cuando cargas los documentos):

- Cargas los documentos
- Los limpias y troceas en chunks
- Conviertes cada chunk en un embedding
- Guardas todo en el vector store

**Fase de consulta** (Cada vez que alguien pregunta):

- Llega una pregunta
- La conviertes en embedding
- Buscas en el vector store los chunks más similares
- Construyes un prompt con la pregunta y los chunks
- El LLM genera la respuesta final


## 3 - Qué son los embeddings

Un embedding es una forma de convertir texto en números para que un ordenador pueda comparar significados.

Por ejemplo, las frases "el perro corre" y "el caballo trota" tienen palabras distintas pero significados parecidos. 
Un modelo de embeddings las convierte en listas de números (vectores) que estarán muy cerca entre sí en el espacio 
matemático. En cambio "el perro corre" y "antonio fluye" tendrán vectores muy lejanos.

Esto permite buscar por **significado** en vez de por palabras exactas, que es lo que hace que RAG sea tan potente. 
El modelo que usaremos es `sentence-transformers/all-MiniLM-L6-v2`, que convierte cualquier texto en un vector de 384 números.


## 4 - Qué es un vector store

Es una base de datos especializada en guardar y buscar vectores. A diferencia de una base de datos SQL que busca 
por coincidencia exacta de texto, un vector store busca por **similitud matemática** entre vectores.

Cuando haces una pregunta, se convierte en un vector y el vector store encuentra los chunks cuyos vectores 
están más cerca matemáticamente, es decir, los más similares en significado. 

Usaremos **ChromaDB**, que es local, gratuito y no necesita servidor externo.


## 5 - Pros y contras de los modelos

**Phi-3-mini** (el que usaremos)

- Muy ligero, 2GB, funciona con poca RAM
- Respuestas rápidas
- Bueno para tareas concretas y bien definidas
- Menos potente que modelos más grandes
- Puede tener problemas con preguntas muy complejas

**Llama 3.2 3B**

- Buen equilibrio entre tamaño y calidad
- Recomendado como primera opción
- Necesita mínimo 8GB RAM
- Más lento que Phi-3-mini

**Mistral 7B**

- El más potente de los tres
- Mejores respuestas en tareas complejas
- Necesita 16GB RAM o más
- Lento sin GPU


## 6 - Cómo descargar contenido de Confluence

Hay 2 formas:

**Exportación manual** - desde la interfaz de Confluence podemos exportar páginas como HTML o PDF. Es lo más sencillo 
para el MVP. Vas a la página, le das a exportar, y guardas el archivo en `data/raw/`.

**API REST de Confluence** - Confluence tiene una API que permite descargar páginas programáticamente. Necesitamos 
un token de acceso y la URL de tu instancia. 

Es más potente porque puedes automatizar la descarga de todas las páginas, pero requiere credenciales y algo más de código.
Para el MVP la exportación manual es suficiente.

Para este proyecto usaremos la exportación manual porque es más rápido de implementar y el objetivo es construir 
el RAG, no el conector de Confluence.


## 7 - Propuesta de arquitectura

El flujo completo es este:
```
FASE DE INDEXACIÓN
Confluence - data/raw/ - Limpieza - data/clean/ - Chunks - Embeddings - ChromaDB

FASE DE CONSULTA
Pregunta - Embedding - ChromaDB (top-3 chunks) - Prompt - Phi-3-mini - Respuesta
