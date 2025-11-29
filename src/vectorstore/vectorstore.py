import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from src.utils import load_config

class VectorStore():
    def __init__(self, path: str, collection: str, embedder):
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(name=collection)

        self.embedder = embedder

    def query(self, user_query: str, n_results: int):
        query_embeddings = self.embedder.encode([user_query])

        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
        )
        contexts = [doc for doc in results["documents"][0]]
        return contexts

    def rag_query(self, user_query: str, n_results: int):
        contexts = self.query(user_query, n_results)
        context_text = "\n\n".join(contexts)

        prompt = f"""Answer the question using the context below.

        Context:
        {context_text}

        Question: {user_query}
        Answer:"""

        return prompt
    
def get_vectorstore():
    config=load_config()
    embedder = SentenceTransformer(config["embedding"]["model_name"])
    vectorstore = VectorStore(
        path=config["vec_db"]["root_dir"],
        collection="docs",
        embedder=embedder,
    )
    return vectorstore