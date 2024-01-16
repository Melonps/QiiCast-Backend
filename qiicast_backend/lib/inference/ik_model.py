import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle

class IkModel:
    def __init__(self, model_path: str) -> None:
        """
        コンストラクタ
        :param model_path: 保存されたLightGBMモデルのファイルパス
        """
        self.model_lightGBM = pickle.load(open(model_path, "rb"))

    def _process_data(self, data_meta: dict) -> pd.DataFrame:
        """
        データの前処理を行うメソッド
        :param data_meta: 予測に必要なメタデータを含む辞書
        :return: 前処理済みのデータが格納されたDataFrame
        """
        user_data = data_meta.get("user", {})
        data = {
            "user_items_count": [user_data.get("items_count", 0)],
            "user_followers_count": [user_data.get("followers_count", 0)],
        }
        return pd.DataFrame(data)

    def predict(self, df_meta: pd.DataFrame) -> np.ndarray:
        """
        予測を行うメソッド
        :param df_meta: 前処理済みのデータが格納されたDataFrame
        :return: 予測結果の配列
        """
        preprocess_data = self._process_data(df_meta)
        # LightGBMモデルで予測を行う
        # num_iteration に best_iteration を指定して最適なラウンドでの予測を行う
        prediction = self.model_lightGBM.predict(
            preprocess_data, num_iteration=self.model_lightGBM.best_iteration
        )
        return prediction[0]
