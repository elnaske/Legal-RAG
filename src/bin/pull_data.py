import argparse

# data gathering imports
from src.ingestion import CourtListenerAPI, save_to_json

# SQL related imports
from src.vectorstore import init_db, sql_db_upsert


def pull_data(max_pages: int = 1) -> None:
    """Pull data using CourtListener API. Saves opinion results to a .json file that is stored in the chroma vector db. Pushes cluster and opinion metadata to SQL relational db.

    Args:
        max_pages (int): Maximum number of pages on CourtListener to parse through.
    """
    # CourtListener API:
    # Dockets > Clusters > Opinions
    # Text is in opinions (either plain text, html, or xml; latter two preferred for parsing)
    # Metadata is split across all three and sometimes redundant (e.g. dockets and clusters contain case names, but opinions don't)

    # ensure db is initialized
    init_db()

    api = CourtListenerAPI()

    # setting up datapull to iterate through mult. pages on CourtListener
    url = "search"
    params = {"q": "criminal"}

    # iterating through the mult. pages
    for i in range(max_pages):
        query_r = api.call(url, params)
        if query_r.status_code == 200:
            q_data = query_r.json()

            # printing total results on just first page
            if i == 0:
                print("Total Results:", q_data["count"])

            print(f"\n{'*' * 20}\nPulling Page #{i + 1} of {max_pages}\n{'*' * 20}")
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

            # once we go through one page, set the url to the next one:
            print(f"\nPage #{i + 1} done.")
            url = q_data["next"]
            # setting params to none will use the same query as before
            params = None

        else:
            print("Error:", query_r.status_code, query_r.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Max number of search result pages to fetch (default: 1 page)",
    )
    args = parser.parse_args()

    pull_data(max_pages=args.max_pages)
