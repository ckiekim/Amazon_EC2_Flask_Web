# MNIST 손글씨 모델
import pandas as pd 
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

df_train = pd.read_csv('../static/data/digits_train.csv')
X_train = df_train.iloc[:, :-1].values
y_train = df_train.iloc[:, -1].values
print(X_train.shape, y_train.shape)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
joblib.dump(scaler, '../static/model/digits_scaler.pkl')

# 1. Logistic Regression
lr_clf = LogisticRegression(max_iter=300)
params = {
    #'C': [0.1, 1, 5, 10]
    #'C': [2, 3, 4, 5, 6, 7]
    'C': [1.5, 2, 3]
}
grid_cv = GridSearchCV(lr_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('1. Logistic Regression')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_lr = grid_cv.best_estimator_
joblib.dump(best_lr, '../static/model/digits_lr.pkl')

# 2. SVM
sv_clf = SVC()
params = {
    #'C': [0.1, 1, 5, 7, 10]
    'C': [3, 4, 5, 6, 7]
}
grid_cv = GridSearchCV(sv_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('2. SVM')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_sv = grid_cv.best_estimator_
joblib.dump(best_sv, '../static/model/digits_sv.pkl')

# 3. Random Forest
rf_clf = RandomForestClassifier(random_state=2021)
params = {
    #'max_depth': [4, 6, 8, 10],
    #'max_depth': [8, 12, 14, 16],
    'max_depth': [14, 16, 18, 20],
    'min_samples_split': [2, 3, 4]
}
grid_cv = GridSearchCV(rf_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('3. Random Forest')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_rf = grid_cv.best_estimator_
joblib.dump(best_rf, '../static/model/digits_rf.pkl')
