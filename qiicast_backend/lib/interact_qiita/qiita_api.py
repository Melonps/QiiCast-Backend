import yaml
import pandas as pd
import requests
from typing import Optional, List, Dict, Union


def load_config(path: str) -> Dict[str, Union[str, Dict[str, str]]]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_api_token(secret_path: str) -> str:
    secrets = load_config(secret_path)
    return secrets.get("qiita_v2", {}).get("access_token", "")


def request_page(
    data_to: str, data_from: str, page_number: int, per_page: int
) -> Optional[List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]]:
    """Qiita APIから特定日の記事をn件取得し、JSON形式で保存する

    Parameters
    ----------
    data_to : str
        取得したい記事の日付の上限（例: "2024-01-01"）
    data_from : str
        取得したい記事の日付の下限（例: "2024-01-01"）
    page_number : int
        取得するページの数。
    per_page : int
        1ページあたりの記事数。

    Returns
    -------
    Optional[List[Dict[str, Union[str, int, float, List[Union[str, int, float]]]]]]:
        取得した記事データのリスト。エラーが発生した場合はNone。
    """
    api_token = get_api_token("conf/secret.yml")  # パスは適宜変更
    if not api_token:
        print("APIトークンが見つかりません。設定ファイルを確認してください。")
        return None

    headers = {"Authorization": f"Bearer {api_token}"}
    base_url = f"https://qiita.com/api/v2/items?page={page_number}&per_page={per_page}&query=created%3A%3E%3D{data_from}+created%3A%3C%3D{data_to}"
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return None

    # レスポンスをJSON形式で取得
    return response.json()
