import chromadb
from chromadb.config import Settings

class VectorStore():
    def __init__(self, path: str, collection: str, embedder):
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(name=collection)

        self.embedder = embedder

    def rag_query(self, user_query: str, n_results: int):
        query_embeddings = self.embedder.encode([user_query])

        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
        )
        contexts = [doc for doc in results["documents"][0]]

        context_text = "\n\n".join(contexts)

        prompt = f"""Answer the question using the context below.

        Context:
        {context_text}

        Question: {user_query}
        Answer:"""

        return prompt