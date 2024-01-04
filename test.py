from qiicast_backend.lib.interact_qiita.qiita_api import request_page
from qiicast_backend.lib.data_collection.collection import (
    ArticleCollector,
)
import pprint

# request test
# pprint.pprint(
#     request_page(
#         data_from="2023-01-01", data_to="2023-01-02", page_number=10, per_page=2
#     )
# )

# request articles and save as csv
path = f"output_result/test_result.csv"
collector = ArticleCollector(max_pages=20)
collector.collect_qiita_articles_by_date()
collector.save_as_csv(result_csv_path=path)
# collector.save_as_json(result_json_path="output_result/test_result.json")
