# Train/Test dataset 만들기
# 군집화/PCA 사용할 데이터셋 포함
import pandas as pd 
import sklearn.datasets as sd
from sklearn.model_selection import train_test_split

# 아이리스 데이터셋
iris = sd.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
X_train, X_test, y_train, y_test = train_test_split(
    df, iris.target, test_size=0.25, stratify=iris.target, random_state=2021
)
X_train.to_csv('static/data/iris_train.csv', index=False)
X_test.to_csv('static/data/iris_test.csv', index=False)
df.to_csv('static/clus_pca_data/iris.csv', index=False)     # 군집화

# 와인 데이터셋
wine = sd.load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['target'] = wine.target
X_train, X_test, y_train, y_test = train_test_split(
    df, wine.target, test_size=0.25, stratify=wine.target, random_state=2021
)
X_train.to_csv('static/data/wine_train.csv', index=False)
X_test.to_csv('static/data/wine_test.csv', index=False)
df.to_csv('static/clus_pca_data/wine.csv', index=False)     # 군집화

# MNIST Digit 데이터셋
digits = sd.load_digits()
df = pd.DataFrame(digits.data, columns=digits.feature_names)
df['target'] = digits.target
X_train, X_test, y_train, y_test = train_test_split(
    df, digits.target, test_size=0.25, stratify=digits.target, random_state=2021
)
X_train.to_csv('static/data/digits_train.csv', index=False)
X_test.to_csv('static/data/digits_test.csv', index=False)

# 유방암 데이터셋
cancer = sd.load_breast_cancer()
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df['target'] = cancer.target
X_train, X_test, y_train, y_test = train_test_split(
    df, cancer.target, test_size=0.25, stratify=cancer.target, random_state=2021
)
X_train.to_csv('static/data/cancer_train.csv', index=False)
X_test.to_csv('static/data/cancer_test.csv', index=False)
df.to_csv('static/clus_pca_data/breast_cancer.csv', index=False)     # 군집화

# 당뇨병 데이터셋
diabetes = sd.load_diabetes()
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df['target'] = diabetes.target
X_train, X_test, y_train, y_test = train_test_split(
    df, diabetes.target, test_size=0.25, random_state=2021
)
X_train.to_csv('static/data/diabetes_train.csv', index=False)
X_test.to_csv('static/data/diabetes_test.csv', index=False)

# Boston 데이터셋
boston = sd.load_boston()
df = pd.DataFrame(boston.data, columns=boston.feature_names)
df['target'] = boston.target
X_train, X_test, y_train, y_test = train_test_split(
    df, boston.target, test_size=0.25, random_state=2021
)
X_train.to_csv('static/data/boston_train.csv', index=False)
X_test.to_csv('static/data/boston_test.csv', index=False)

# 타이타닉 데이터셋

# 피마 인디언 데이터셋
