import requests
from dotenv import load_dotenv
import os
import json

# SQL db stuff
from .SQLite_db import SessionLocal
from .db_model import Cluster, Opinions


class CourtListenerAPI:
    def __init__(self):
        self.headers = {"Authorization": f"Token {self.get_api_key()}"}
        self.root_url = "https://www.courtlistener.com/api/rest/v4/"

    def get_api_key(self):
        load_dotenv()

        API_KEY = os.getenv("COURTLISTENER_API_KEY")
        if API_KEY is None:
            print("Enter CourtListener API token:")
            API_KEY = input()

        return API_KEY

    def call(self, url, params=None):
        if not url.startswith("http"):
            url = os.path.join(self.root_url, url)

        response = requests.get(url, params=params, headers=self.headers)
        return response


def save_to_json(d):
    # -- TO DO:
    # ---- USE DIR FROM CONFIG.YAML INSTEAD

    if any([d["plain_text"], d["html"], d["html_with_citations"], d["xml_harvard"]]):

        if not os.path.exists("./data"):
            os.makedirs("./data/raw/opinions")

        with open(f"./data/raw/opinions/{d['id']}.json", "w") as f:
            json.dump(d, f)
    else:
        print("No text found. Skipping...")


# upserting the Cluster and Opinion data to SQLdb
def sql_db_upsert(cluster_json, opinion_json):
    pass


def main():
    # CourtListener API:
    # Dockets > Clusters > Opinions
    # Text is in opinions (either plain text, html, or xml; latter two preferred for parsing)
    # Metadata is split across all three and sometimes redundant (e.g. dockets and clusters contain case names, but opinions don't)

    api = CourtListenerAPI()

    query_r = api.call("search", params={"q": "copyright"})

    if query_r.status_code == 200:
        q_data = query_r.json()

        print("Total Results:", q_data["count"])

        for result in q_data["results"]:
            print("-" * 20)
            print(result["cluster_id"], result["caseName"])

            cluster_r = api.call(f"clusters/{result['cluster_id']}")
            c_data = cluster_r.json()

            for opinion in c_data["sub_opinions"]:
                print(opinion)

                opinion_r = api.call(opinion)

                save_to_json(opinion_r.json())
    else:
        print("Error:", query_r.status_code, query_r.text)


if __name__ == "__main__":
    main()
