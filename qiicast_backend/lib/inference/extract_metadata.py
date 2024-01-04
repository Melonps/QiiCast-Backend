import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
API_KEY = os.getenv("API_KEY")


jsonfile = "03list.json"
# 列をフラット化する際の区切り文字
sep = "."


# フラット化
def flatten(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        # 列名の生成
        new_key = parent_key + sep + k if parent_key else k
        # 辞書型項目のフラット化
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        # リスト項目のフラット化
        elif isinstance(v, list):
            new_key_tmp = new_key
            for i, elm in enumerate(v):
                new_key = new_key_tmp + sep + str(i)
                # リストの中の辞書
                if isinstance(elm, dict):
                    items.extend(flatten(elm, new_key, sep=sep).items())
                # 単なるリスト
                else:
                    items.append((new_key, elm))
        # 値追加
        else:
            items.append((new_key, v))
    return dict(items)


def get_qiita_articles(api_token):
    api_url = "https://qiita.com/api/v2/items"

    headers = {"Authorization": f"Bearer {api_token}"}
    params = {"per_page": 100, "page": 1}

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    articles = response.json()
    delete_columns = [
        "rendered_body",
        "created_at",
        "group",
        "id",
        "private",
        "reactions_count",
        "updated_at",
        "slide",
        "team_membership",
        "organization_url_name",
        "url",
        "coediting",
    ]
    for article in articles:
        for column in delete_columns:
            article.pop(column, None)
    json_file = open("test.json", "w")
    json.dump(articles, json_file)

    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Tags: {', '.join(tag['name'] for tag in article['tags'])}")
        print("-" * 30)
    # フラット化

    dlist = []
    for di in articles:
        dlist.append(flatten(di, sep=sep))

    # print(dlist)
    df = pd.DataFrame.from_dict(dlist)
    df.to_csv("test.csv", index=False)


if __name__ == "__main__":
    get_qiita_articles(API_KEY)
