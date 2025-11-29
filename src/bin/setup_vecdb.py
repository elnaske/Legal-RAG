from glob import glob
import json

from src.preprocessing import Preprocessor
from src.vectorstore import get_vectorstore
from src.utils import load_config

def main():
    config = load_config()

    data_root = config["data"]["root_dir"]

    vectorstore = get_vectorstore()

    preprocessor = Preprocessor(
        text_splitter=config["preprocessing"]["text_splitter"],
        chunking_args=config["preprocessing"]["chunking_args"], 
        embedder=vectorstore.embedder,
    )
    opinion_paths = glob(f"{data_root}/raw/opinions/*.json")

    i = 0

    for path in opinion_paths:
        with open(path, "r") as f:
            opinion = json.load(f)
        doc = preprocessor(opinion)
        if doc is not None:
            vectorstore.collection.add(**doc)
            print(f"Opinion {opinion["id"]} successfully added to vector database")
            i += 1

    print(f"\nPreprocessing finished.\nAdded {i}/{len(opinion_paths)} opinions")

if __name__=="__main__":
    main()