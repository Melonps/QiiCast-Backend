from qiicast_backend.lib.interact_qiita.qiita_api import request_page
import pprint

# request test
pprint.pprint(
    request_page(
        data_from="2023-01-01", data_to="2023-01-02", page_number=10, per_page=2
    )
)
