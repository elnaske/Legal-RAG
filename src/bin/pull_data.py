# import requests
# from dotenv import load_dotenv
# import os
# import json

# data gathering imports
from src.ingestion import CourtListenerAPI, save_to_json

# SQL related imports
from src.vectorstore import init_db, sql_db_upsert


def pull_data():
    # CourtListener API:
    # Dockets > Clusters > Opinions
    # Text is in opinions (either plain text, html, or xml; latter two preferred for parsing)
    # Metadata is split across all three and sometimes redundant (e.g. dockets and clusters contain case names, but opinions don't)

    # ensure db is initialized
    init_db()

    api = CourtListenerAPI()

    query_r = api.call("search", params={"q": "criminal"})

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
                o_data = opinion_r.json()

                save_to_json(opinion_r.json())

                # also pushing to db
                sql_db_upsert(c_data, o_data)

    else:
        print("Error:", query_r.status_code, query_r.text)


if __name__ == "__main__":
    pull_data()
