import chromadb
from chromadb.config import Settings


def vector_storage():
    client = chromadb.Client(
        Settings(anonymized_telemetry=False),
    )

    collection = client.create_collection(name="docs")

    # Add embeddings
    collection.add(
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"n": n} for n in range(len(chunks))],
    )
    # --------------------------
