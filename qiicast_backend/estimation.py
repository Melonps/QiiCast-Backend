import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split

# variable
test_size = 0.2  # 0 < test_size < 1
random_state = 0
train_data_csv_filename = "./articles_metadata_20000_2022-12-01_2023-01-31.csv" 

# import train data
train_df = pd.read_csv(train_data_csv_filename,  encoding='UTF-8')

# get train parameters
features_df = pd.concat([train_df["user.items_count"], train_df["user.followers_count"]], axis=1)  # �����ʂ̓��[�U�[�̓��e���ƃt�H�����[��
features_df = pd.concat([features_df, train_df["likes_count"]], axis=1)  # �\���͂����ː��̂�
x_train, x_test, y_train, y_test = train_test_split(features_df.iloc[:,:2], features_df.iloc[:,2:], test_size=test_size, random_state=random_state)  # �S�f�[�^�g���������悳�����ł͂���
train_set = lgb.Dataset(x_train, y_train)
test_set = lgb.Dataset(x_test, y_test)

# train 
params = {'metric' : 'rmse'}
model = lgb.train(params, train_set)

# predict
y_pred = model.predict(x_test)

# accuracy
accuracy = 0
for i in range(len(y_pred)):  # �����ː��� 5 �ȏォ�����łȂ����̕���
  if(y_test_np[i][0] >= 5 and y_pred[i] >= 5): accuracyuracy += 1
  if(y_test_np[i][0] < 5 and y_pred[i] < 5): accuracy += 1
print("Accuracy:", accuracy / len(y_pred))
