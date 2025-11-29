from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import uuid

from src.utils import load_config
from src.preprocessing import chunk_html
from src.vectorstore import VectorStore

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

vecdb = VectorStore(
    path=config["vec_db"]["root_dir"],
    collection="docs",
    embedder=embedder,
)

TEST_FILE = "./data/raw/opinions/9951612.json"
# TEST_FILE = "./data/raw/opinions/782535.json"
chunks = chunk_html(TEST_FILE)
embeddings = embedder.encode(chunks)

vecdb.collection.add(
    ids=[str(uuid.uuid4()) for _ in chunks],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"n": n} for n in range(len(chunks))],
)

query_texts = ["What does 'AIM' mean?", "What are the components of Aimster?"]

rag_prompt = vecdb.rag_query(query_texts[0], n_results=3)

response = llm_pipeline(rag_prompt)[0]["generated_text"]

print(response)
