

import csv
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#フィールドサイズ変更　デフォルト：128KB
csv.field_size_limit(100000000)       #100MB

body = 0
comments_count = 1
likes_count = 2
stocks_count = 3
title = 7
user_followees_count = 10
user_followers_count = 11
page_view_count = 24
count = 0
#######################
X = np.zeros((10000, 5))
y = np.zeros(10000)

csv_file_path = 'data/articles_metadata_20000_2022-12-01_2023-01-31.csv'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    next(csv_reader)
    
    for row in csv_reader:
        print(count)
        X[count] = float(row[user_followees_count]), float(row[user_followers_count]), float(len(row[title])), float(len(row[body])), float(row[comments_count])
        y[count] = float(row[likes_count])
        count += 1
        
        """
        count += 1
        print(count)
        print(row[likes_count])
        print(row[stocks_count])
        print(row[user_followees_count])
        print(row[user_followers_count])
        print(row[title])
        print()
        """


####################################################################
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=2024)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0, random_state=2024)

model = LinearRegression()
model.fit(X_train, y_train)

# テストデータでの予測
y_pred = model.predict(X_test)

# モデルの評価
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 予測結果の可視化（2次元の場合の例）
"""
plt.scatter(X_test[:, 4], y_test, color='blue', label='True values')
plt.scatter(X_test[:, 4], y_pred, color='red', label='Predictions')
plt.xlabel('comments_count')
plt.ylabel('Like')
"""
#"""
plt.scatter(X_test[:, 3], y_test, color='blue', label='True values')
plt.scatter(X_test[:, 3], y_pred, color='red', label='Predictions')
plt.xlabel('len(body)')
plt.ylabel('Like')
#"""
plt.legend()
plt.show()


# モデルの保存
with open('qiicast_backend/model/nobo_model.pkl', 'wb') as file:
    pickle.dump(model, file)