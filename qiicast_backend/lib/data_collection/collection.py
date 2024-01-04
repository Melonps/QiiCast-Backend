from qiicast_backend.lib.interact_qiita.qiita_api import request_page
from typing import Optional, List, Dict, Union
import dataclasses
import pandas as pd
import json

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
    per_page: int
    from_date: str
    to_date: str
    result_json: Optional[
        List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]
    ] = None
    """
        Initialize the ArticleCollector.

        Parameters
        ----------
        max_pages : int
            The maximum number of pages to collect.
        per_page : int
            The number of articles per page.
        from_date : str
            The starting date for collecting articles.
        to_date : str
            The ending date for collecting articles.
        """

    def collect_qiita_articles_by_date(
        self,
    ) -> None:
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
                    data_from=self.from_date,
                    data_to=self.to_date,
                    page_number=page_index,
                    per_page=self.per_page,
                )
                if each_result == []:
                    print("No more articles for this date range.")
                    break
                all_result.extend(each_result)
                current_page_number += self.per_page
                page_index += 1
                print(f"PAGE {current_page_number}/{self.max_pages} DONE")
            except:
                print("API request error")
                break
        self.result_json = all_result

    def preprocess_result(self):
        """Preprocesses the collected Qiita article data by removing specified columns."""
        for article in self.result_json:
            for column in delete_columns:
                article.pop(column, None)

    def save_as_json(self, result_json_path: str):
        """Saves the preprocessed Qiita article data as a JSON file.

        Parameters
        ----------
        result_json_path : str
            The path to save the JSON file.
        """
        self.preprocess_result()
        json_file = open(result_json_path, "w")
        json.dump(self.result_json, json_file)

    def save_as_csv(self, result_csv_path: str):
        """Saves the preprocessed Qiita article data as a CSV file.

        Parameters
        ----------
        result_csv_path : str
            The path to save the CSV file.
        """
        self.preprocess_result()
        dic_list = []

        for di in self.result_json:
            dic_list.append(flatten(result_json=di, parent_key="", sep=sep))
        df = pd.DataFrame.from_dict(dic_list)
        print(df.columns)
        print(df.shape)
        print(df.tail(1))

        df.to_csv(result_csv_path, index=False)


def flatten(result_json, parent_key, sep=sep):
    """Flattens a nested dictionary or list into a flat dictionary.

    Parameters
    ----------
    result_json : dict
        The nested dictionary or list to be flattened.
    parent_key : str
        The parent key of the nested dictionary or list.
    sep : str, optional
        The separator used between keys, by default ".".

    Returns
    -------
    dict
        The flattened dictionary.
    """
    parent_key = ""
    items = []
    for k, v in result_json.items():
        # Column name generation
        new_key = parent_key + sep + k if parent_key else k
        # Flatten dictionary items
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        # Flatten list items
        elif isinstance(v, list):
            new_key_tmp = new_key
            for i, elm in enumerate(v):
                new_key = new_key_tmp + sep + str(i)
                # Dictionary within the list
                if isinstance(elm, dict):
                    items.extend(flatten(elm, new_key, sep=sep).items())
                # Simple list
                else:
                    items.append((new_key, elm))
        else:
            items.append((new_key, v))
    return dict(items)
