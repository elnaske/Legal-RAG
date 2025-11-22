import uuid
from glob import glob
import chromadb
from chromadb.config import Settings


def vector_storage(chunks: list[str], embeddings) -> None:
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
