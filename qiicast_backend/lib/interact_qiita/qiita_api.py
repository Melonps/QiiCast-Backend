import json
import yaml
import requests
from typing import Optional

if True:
    SCRT = yaml.safe_load(open("qiicast_backend/conf/secret.yml", "r"))
    API_TOKEN = SCRT["qiita_v2"]["access_token"]

def request_page(tag: Optional[str]) -> None:    
    """Qiita APIから記事を取得し、JSON形式で保存する

    Parameters
    ----------
    save_path : str
        保存先のパス
    tag : Optional[str]
        タグ名。とりあえず高々1つ    
    """

    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    url = f'https://qiita.com/api/v2/items?page=1&per_page=100'
    if tag:
        url += "&query=tag%3A" + tag
    response = requests.get(url, headers=headers)

    return response.json()