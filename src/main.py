import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import uuid
from glob import glob

from utils import load_config
from ingestion.chunking import chunk_html

config = load_config()

embedder = SentenceTransformer(config["embedding"]["model_name"])
print("embedding model loaded")
tokenizer = AutoTokenizer.from_pretrained(
    config["llm"]["model_name"], trust_remote_code=True
)
print("tokenizer loaded")
llm = AutoModelForCausalLM.from_pretrained(
    config["llm"]["model_name"], device_map="auto", dtype="auto", trust_remote_code=True
)
print("LLM loaded")

llm_pipeline = pipeline(
    "text-generation", model=llm, tokenizer=tokenizer, max_new_tokens=512
)
print("pipeline set up")


def rag_query(user_query):
    query_embeddings = embedder.encode([user_query])

    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=3,
    )
    contexts = [doc for doc in results["documents"][0]]

    context_text = "\n\n".join(contexts)

    prompt = f"""Answer the question using the context below.

    Context:
    {context_text}

    Question: {user_query}
    Answer:"""

    response = llm_pipeline(prompt)[0]["generated_text"]

    return response


TEST_FILE = "./data/raw/opinions/9951612.json"
chunks = chunk_html(TEST_FILE)
embeddings = embedder.encode(chunks)

# --- MOVE TO INGESTION ---
# ---- vectorstore.py ----
client = chromadb.Client(Settings(anonymized_telemetry=False))

collection = client.create_collection(name="docs")

# Add embeddings
collection.add(
    ids=[str(uuid.uuid4()) for _ in chunks],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"n": n} for n in range(len(chunks))],
)
# --------------------------

query_texts = ["What does 'AIM' mean?", "What are the components of Aimster?"]

response = rag_query(query_texts[0])

print(response)
