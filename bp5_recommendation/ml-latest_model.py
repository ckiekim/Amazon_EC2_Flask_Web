import joblib
import pandas as pd
from surprise import SVD, Reader
from surprise.dataset import DatasetAutoFolds

ratings = pd.read_csv('../static/data/ml-latest/ratings.csv')
reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0.5,5))
data_folds = DatasetAutoFolds('../static/data/ml-latest/ratings_noh.csv', reader=reader)
# 전체 데이터를 학습 데이터로 사용
trainset = data_folds.build_full_trainset()
# 모델 생성 및 학습
model = SVD(n_epochs=20, n_factors=50, random_state=2022)
model.fit(trainset)
joblib.dump(model, '../static/model/movie-surprise.pkl')