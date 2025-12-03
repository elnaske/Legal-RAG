import json
import os

import requests
from dotenv import load_dotenv


class CourtListenerAPI:
    """API object that allows for connection to pull Courtlistener data.

    Attributes:
        headers (str): Header that uses os env API key for authorization
        root_url (str): Static root URL to courlistener site. Essentially const.
    """

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
