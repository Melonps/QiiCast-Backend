from qiicast_backend.lib.data_collection.collection import (
    ArticleCollector,
)

FROM_DATE = "2022-12-01"
TO_DATE = "2023-01-31"
MAX_PAGES = 10000  # 最大で10000ページまで取得可能
PER_PAGE = 100

path = f"output_result/articles_metadata_{MAX_PAGES}_{FROM_DATE}_{TO_DATE}.csv"
collector = ArticleCollector(
    max_pages=MAX_PAGES, per_page=PER_PAGE, from_date=FROM_DATE, to_date=TO_DATE
)
collector.collect_qiita_articles_by_date()
collector.save_as_csv(result_csv_path=path)
