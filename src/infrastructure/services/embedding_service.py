from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingService:

    def __init__(self, model_name: str):
        print(f"[+] Inicializando modelo de embeddings: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}
        )

    def get_embedding_function(self):
        return self.embeddings
