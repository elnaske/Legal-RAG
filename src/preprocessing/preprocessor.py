from langchain_text_splitters import RecursiveCharacterTextSplitter, SpacyTextSplitter
import uuid
from typing import Union

from src.preprocessing.chunking import parse_html

class Preprocessor:
    def __init__(self, text_splitter: str, chunking_args: dict, embedder) -> None:
        if text_splitter == "spacy":
            self.text_splitter = SpacyTextSplitter(**chunking_args)
        else:
            self.text_splitter = RecursiveCharacterTextSplitter(**chunking_args)

        self.embedder = embedder

    def __call__(self, opinion: dict) -> Union[dict, None]:
        """
        Runs preprocessing steps based on provided configuration.

        Args:
            opinion (dict): output returned by API
        Returns:
            A dict containing text, embeddings, and metadata for all chunks. Intended to be used as input to vector DB.
        """
        # check for html
        if not opinion.get("html"):
            print(f"Opinion {opinion["id"]} has no HTML text. Skipping...")
            return None
        
        html = opinion["html"]

        paragraphs = parse_html(html)

        chunks = self.chunk(paragraphs)

        embs = self.get_embeddings(chunks)

        metadatas = [{"n": n} for n in range(len(chunks))]

        return {
            "ids": [(str(uuid.uuid4())) for _ in chunks],
            "documents": chunks,
            "embeddings": embs,
            "metadatas": metadatas,
        }
    
    def chunk(self, raw_text: Union[str, list[str]]) -> list[str]:
        """
        Splits raw text into chunks.
        """
        if isinstance(raw_text, str):
            raw_text = [raw_text]

        texts = self.text_splitter.create_documents(raw_text)
        chunks = [t.page_content for t in texts] 
        return chunks
    
    def get_embeddings(self, chunks):
        """
        Gets embeddings for the chunks.
        """
        return self.embedder.encode(chunks)