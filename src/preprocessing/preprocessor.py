from langchain_text_splitters import RecursiveCharacterTextSplitter, SpacyTextSplitter
import uuid
from pathlib import Path
import re
from typing import Union, Dict

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
                raw_text = re.sub(r"\s\s+", "\n ", raw_text)
                paragraphs = raw_text.split("\n")
            else:
                print(f"Opinion {opinion["id"]} has no text. Skipping...")
                return None

        chunks = self.chunk(paragraphs)

        if not chunks:
            print(f"Opinion{ opinion["id"]}: No chunks. Skipping...")
            return None

        embs = self.get_embeddings(chunks)

        doc_metadata = self.extract_doc_metadata(opinion)

        metadatas = []
        for n in range(len(chunks)):
            chunk_dict = doc_metadata.copy()
            chunk_dict["n"] = n
            metadatas += [chunk_dict]

        return {
            "ids": [(str(uuid.uuid4())) for _ in chunks],
            "documents": chunks,
            "embeddings": embs,
            "metadatas": metadatas,
        }

    def extract_doc_metadata(self, opinion: dict) -> dict:
        """
        Extracts metadata from opinion document:
        - Case name
        - Decision date
        """
        path = opinion.get("local_path")
        if path:
            parts = Path(path).parts
            year, month, day, name = parts[1:]

            name = name[:-4] # cut off .pdf
            name = name.replace("_", " ")
        else:
            year, month, day, name = "unk", "unk", "unk", "unk"

        metadata = {
            "year": year,
            "month": month,
            "day": day,
            "casename": name,
        }

        return metadata


    def chunk(self, raw_text: Union[str, list[str]]) -> list[str]:
        """
        Splits raw text into chunks.
        """
        if isinstance(raw_text, str):
            raw_text = [raw_text]

        raw_text = " ".join(raw_text)

        # texts = self.text_splitter.create_documents(raw_text)
        # chunks = [t.page_content for t in texts] 
        # return chunks

        texts = self.text_splitter.split_text(raw_text)
        return texts
    
    def get_embeddings(self, chunks):
        """
        Gets embeddings for the chunks.
        """
        return self.embedder.encode(chunks)