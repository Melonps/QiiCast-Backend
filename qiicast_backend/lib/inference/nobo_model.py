import csv
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle


class NoboModel:
    def __init__(self, model_path: str) -> None:
        """
        コンストラクタ
        :param model_path: 保存されたリニアモデルのファイルパス
        """
        self.model_linear = pickle.load(open(model_path, "rb"))

    def _process_data(self, data_meta: dict) -> pd.DataFrame:
        """
        データの前処理を行うメソッド
        :param data_meta: 予測に必要なメタデータを含む辞書
        :return: 前処理済みのデータが格納されたDataFrame
        """
        user_data = data_meta.get("user", {})
        data = {
            "user_followees_count": [user_data.get("followees_count", 0)],
            "user_followers_count": [user_data.get("followers_count", 0)],
            "title_length": [len(data_meta.get("title", ""))],
            "body_length": [len(data_meta.get("body", ""))],
            "comments_count": [data_meta.get("comments_count", 0)],
        }
        print(data)
        return pd.DataFrame(data)

    def predict(self, df_meta: pd.DataFrame) -> np.ndarray:
        """
        予測を行うメソッド
        :param df_meta: 前処理済みのデータが格納されたDataFrame
        :return: 予測結果の配列
        """
        preprocess_data = self._process_data(df_meta)
        prediction = self.model_linear.predict(preprocess_data)
        return prediction[0]
