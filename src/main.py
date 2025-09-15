import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
from glob import glob

from utils import load_config
from ingestion.chunking import chunk_html

config = load_config()

model = SentenceTransformer(config["embedding"]["model_name"])

TEST_FILE = "./data/raw/opinions/782535.json"
chunks = chunk_html(TEST_FILE)
embeddings = model.encode(chunks)

# --- MOVE TO INGESTION ---
# ---- vectorstore.py ----
client = chromadb.Client(Settings(anonymized_telemetry=False))

collection = client.create_collection(name="docs")

# Add embeddings
collection.add(
    ids=[str(uuid.uuid4()) for _ in chunks],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"n": n} for n in range(len(chunks))]
)
#--------------------------

query_texts=[
        "What does 'AIM' stand for?",
        "What are the components of Aimster?"
        ]
query_embeddings = model.encode(query_texts)

results = collection.query(
    query_embeddings=query_embeddings,
    n_results=5,
)

for i, query_results in enumerate(results["documents"]):
    print(f"\nQuery {i}: '{query_texts[i]}'")
    print("\n".join(query_results))