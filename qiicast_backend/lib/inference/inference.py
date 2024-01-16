from lib.inference.ik_model import IkModel
from lib.inference.nobo_model import NoboModel


class InferenceEngine:
    def __init__(self) -> None:
        self._processor = None

    def _initialize_processor(self, model_name: str) -> None:
        """
        モデルの初期化
        """
        if model_name == "ik_model":
            self._processor = IkModel(model_path="./model/ik_model.pkl")
        elif model_name == "nobo_model":
            self._processor = NoboModel(model_path="./model/nobo_model.pkl")
        else:
            raise ValueError("model_name must be 'ik_model' or 'nobo_model'")

    def predict(self, model_name: str, data_meta: dict) -> float:
        """
        予測を行うメソッド
        :param model_name: モデル名
        :param data_meta: 予測に必要なメタデータを含む辞書
        :return: 予測結果
        """
        return self._processor.predict(data_meta)
