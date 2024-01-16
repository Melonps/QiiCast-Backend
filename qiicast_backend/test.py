from lib.interact_qiita.qiita_api import request_page
from lib.inference.ik_model import IkModel

# 推論部分のテストコード
data = (request_page("Python"))
Model = IkModel(model_path="qiicast_backend/model/ik_model.pkl")
edited_data = Model._process_data(data[0])
print(edited_data.head())
print(Model.predict(data[0]))