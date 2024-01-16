from lib.interact_qiita.qiita_api import request_page
from lib.inference.ik_model import IkModel
from lib.inference.nobo_model import NoboModel

# 推論部分のテストコード
data = (request_page("Python"))
#ikさんのモデル
#Model = IkModel(model_path="qiicast_backend/model/ik_model.pkl")

#noboさんのモデル 
Model = NoboModel(model_path="qiicast_backend/model/nobo_model.pkl")

edited_data = Model._process_data(data[0])
print(edited_data.head())
print(Model.predict(data[0]))