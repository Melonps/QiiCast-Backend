from qiicast_backend.lib.interact_qiita.qiita_api import request_page
from qiicast_backend.lib.interact_qiita.result_format import format_json_to_csv
from qiicast_backend.lib.interact_qiita.result_format import flatten
from typing import Optional, List, Dict, Union
import dataclasses
import pandas as pd
import json

PER_PAGE_NUMBER = 10
FROM_DATE = "2023-01-01"
TO_DATE = "2023-02-01"

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
sep = "."


@dataclasses.dataclass
class ArticleCollector:
    max_pages: int
    result_json: Optional[
        List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]
    ] = None

    def collect_qiita_articles_by_date(
        self,
    ) -> Optional[
        List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]
    ]:
        """Collects Qiita articles for a specific date from multiple pages.

        Returns
        -------
        Optional[List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]]:
            List of retrieved article data. Returns None if an error occurs.
        """
        all_result = []
        current_page_number = 0
        page_index = 1
        while current_page_number < self.max_pages:
            try:
                each_result = request_page(
                    data_from=FROM_DATE,
                    data_to=TO_DATE,
                    page_number=page_index,
                    per_page=PER_PAGE_NUMBER,
                )
                if each_result == []:
                    print("No more articles for this date range.")
                    break
                all_result.extend(each_result)
                current_page_number += PER_PAGE_NUMBER
                page_index += 1
                print(f"PAGE {current_page_number}/{self.max_pages} DONE")
            except:
                print("API request error")
                break
        self.result_json = all_result

    def preprocess_result(self):
        for article in self.result_json:
            for column in delete_columns:
                article.pop(column, None)

    def save_as_json(self, result_json_path: str):
        self.preprocess_result()
        json_file = open(result_json_path, "w")
        json.dump(result_json_path, json_file)

    def save_as_csv(self, result_csv_path: str):
        self.preprocess_result()
        dic_list = []

        for di in self.result_json:
            dic_list.append(flatten(di, sep=sep))
        df = pd.DataFrame.from_dict(self.result_json)
        print(df.columns)
        print(df.shape)
        print(df.tail(1))

        df.to_csv(result_csv_path, index=False)


def flatten(result_json, parent_key="", sep="."):
    items = []
    for k, v in result_json.items():
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
