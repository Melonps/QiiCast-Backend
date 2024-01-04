import json
import pandas as pd

sep = "."
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


def format_json_to_csv(result_json):
    for article in result_json:
        for column in delete_columns:
            article.pop(column, None)
    json_file = open("test.json", "w")
    json.dump(result_json, json_file)

    dlist = []
    for di in result_json:
        dlist.append(flatten(di, sep=sep))

    df = pd.DataFrame.from_dict(dlist)
    df.to_csv("test.csv", index=False)


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
        else:
            items.append((new_key, v))
    return dict(items)
