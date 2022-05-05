# IMDB 영화평 감성 분석
import re, joblib
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('../static/movies/labeledTrainData.tsv', header=0, sep='\t', quoting=3)
# <br /> 태그는 공백으로 변환
df['review'] = df.review.str.replace('<br />', ' ')
# 영어 이외의 문자는 공백으로 변환
df['review'] = df.review.apply(lambda x: re.sub('[^a-zA-Z]', ' ', x))

feature_df = df.drop(['id', 'sentiment'], axis=1, inplace=False)
X_train, X_test, y_train, y_test = train_test_split(
    feature_df, df.sentiment, test_size=0.25, random_state=2021
)
print(X_train.shape, X_test.shape)

df_test = pd.DataFrame(X_test, columns=['review'])
df_test['sentiment'] = y_test
# df_test.to_csv('../static/data/IMDB_test.csv', index=False)

# Case 1. CountVectorizer + LogisticRegression
pipeline = Pipeline([
    ('count_vect', CountVectorizer(stop_words='english', max_df=500, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=1))
])
pipeline.fit(X_train.review, y_train)
joblib.dump(pipeline, '../static/model/imdb_count_lr.pkl')
''' pipeline = Pipeline([
    ('count_vect', CountVectorizer(stop_words='english', ngram_range=(1,2))),
    ('lr_clf', LogisticRegression())
])
params = ({
    'count_vect__max_df': [100, 300, 500],
    'lr_clf__C': [1, 5, 10]
})
grid_pipe = GridSearchCV(pipeline, param_grid=params, cv=3,
                         scoring='accuracy', verbose=1, n_jobs=-1)
grid_pipe.fit(X_train.review, y_train)
print(grid_pipe.best_params_, grid_pipe.best_score_)
best_count_lr = grid_pipe.best_estimator_
joblib.dump(best_count_lr, '../static/model/imdb_count_lr.pkl') '''

# Case 2. TfidfVectorizer + SupportVectorMachine
pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(stop_words='english', max_df=500, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=10))
])
pipeline.fit(X_train.review, y_train)
joblib.dump(pipeline, '../static/model/imdb_tfidf_lr.pkl')
''' pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(stop_words='english', ngram_range=(1,2))),
    ('lr_clf', LogisticRegression())
])
params = ({
    'tfidf_vect__max_df': [100, 300, 500],
    'lr_clf__C': [0.1, 1, 10]
})
grid_pipe = GridSearchCV(pipeline, param_grid=params, cv=3,
                         scoring='accuracy', verbose=1, n_jobs=-1)
grid_pipe.fit(X_train.review, y_train)
print(grid_pipe.best_params_, grid_pipe.best_score_)
best_tfidf_lr = grid_pipe.best_estimator_
joblib.dump(best_tfidf_lr, '../static/model/imdb_tfidf_lr.pkl') '''
