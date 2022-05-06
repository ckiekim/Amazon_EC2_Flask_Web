# MNIST 손글씨 모델
import pandas as pd 
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

train=pd.read_csv('../static/data/mnist/mnist_train.csv', header=0, index_col=None)
print(train.shape)

X_train, X_test, y_train, y_test = train_test_split(
    train.iloc[:, 1:], train.label, stratify=train.label, test_size=0.25, random_state=2021
)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

df_test = pd.DataFrame(X_test, columns=train.columns)
df_test['target'] = y_test
df_test.to_csv('../static/data/mnist/mnist_test.csv', index=False)

X_train, _, y_train, _ = train_test_split(
    X_train, y_train, stratify=y_train, test_size=0.4, random_state=2021
)
print(X_train.shape, y_train.shape)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
joblib.dump(scaler, '../static/model/mnist_scaler.pkl')

sv_clf = SVC(C=10)
sv_clf.fit(X_train_scaled, y_train)
joblib.dump(sv_clf, '../static/model/mnist_sv.pkl')
''' sv_clf = SVC()
params = {
    #'C': [0.1, 1, 10]
    'C': [5, 10, 20]
}
grid_cv = GridSearchCV(sv_clf, param_grid=params, scoring='accuracy', cv=5, n_jobs=-1)
grid_cv.fit(X_train_scaled, y_train)
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_sv = grid_cv.best_estimator_
joblib.dump(best_sv, '../static/model/mnist_sv.pkl') '''
