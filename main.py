import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
API_KEY = os.getenv("API_KEY")


def get_qiita_articles(api_token):
    api_url = "https://qiita.com/api/v2/items"

    headers = {"Authorization": f"Bearer {api_token}"}
    params = {"per_page": 10, "page": 1}

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    articles = response.json()
    json_file = open("test.json", "w")
    json.dump(articles, json_file)

    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Tags: {', '.join(tag['name'] for tag in article['tags'])}")
        print("-" * 30)


if __name__ == "__main__":
    get_qiita_articles(API_KEY)
