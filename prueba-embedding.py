from chromadb import PersistentClient

client = PersistentClient(path="vectorstore")
collection = client.get_collection("langchain")

print("Cantidad de documentos:", collection.count())
