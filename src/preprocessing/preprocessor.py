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
        # formats = ["html", "html_lawbox", "html_columbia", "html_anon_2020", "xml_harvard"]
        formats = ["html"]

        # Check for supported formats
        paragraphs = []
        for format in formats:
            if opinion.get(format):
                raw_text = opinion[format]
                paragraphs = parse_html(raw_text)
                break
            # If no markup available, fall back to plain text
            if opinion.get("plain_text"):
                raw_text = opinion["plain_text"]
                paragraphs = raw_text.split("\n")
            else:
                print(f"Opinion {opinion["id"]} has no text. Skipping...")
                return None

        chunks = self.chunk(paragraphs)

        if not chunks:
            print(f"Opinion{ opinion["id"]}: No chunks. Skipping...")
            return None

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