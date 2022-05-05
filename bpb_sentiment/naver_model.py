# 네이버 영화 리뷰 감성 분석
import joblib
import numpy as np 
import pandas as pd 

train_df = pd.read_csv("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", sep='\t')
test_df = pd.read_csv("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", sep='\t')

# train dataset
# 중복 샘플 제거
train_df.drop_duplicates(subset=['document'], inplace=True)
# Null값 제거
train_df.dropna(how = 'any', inplace=True)
train_df['document'].replace('', np.nan, inplace=True)
train_df = train_df.dropna(how = 'any')
print(train_df.shape)
train_df['document'] = train_df['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

# test dataset - 전처리해서 없어질 데이터는 저장하지 않게 함
# 중복 제거
test_df.drop_duplicates(subset=['document'], inplace=True)
# Null 제거
test_df.dropna(how='any', inplace=True)

test_df['new_doc'] = test_df['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
indices = list(test_df['new_doc'] != '')

new_df = test_df.loc[indices,:]
new_df.drop('new_doc', axis=1, inplace=True)
print(new_df.shape)
new_df.to_csv('../static/data/naver/movie_test.tsv', sep='\t', index=False)

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from konlpy.tag import Okt

okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
X_train = []
for sentence in train_df['document']:
    morphs = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = ' '.join([word for word in morphs if not word in stopwords]) # 불용어 제거
    X_train.append(temp_X)
print('Train data 토큰화 완료')
y_train = train_df.label.values

# Case 1. CountVectorizer + LogisticRegression
pipeline = Pipeline([
    ('count_vect', CountVectorizer(max_df=700, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=1))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/naver_count_lr.pkl')
print('Case 1. CountVectorizer + LogisticRegression done.')

# Case 2. CountVectorizer + NaiveBayes
pipeline = Pipeline([
    ('count_vect', CountVectorizer(max_df=700, ngram_range=(1,2))),
    ('nb_clf', MultinomialNB())
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/naver_count_nb.pkl')
print('Case 2. CountVectorizer + NaiveBayes done.')

# Case 3. TfidfVectorizer + LogisticRegression
pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(max_df=700, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=10, max_iter=300))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/naver_tfidf_lr.pkl')
print('Case 3. TfidfVectorizer + LogisticRegression done.')

# Case 4. TfidfVectorizer + NaiveBayes
pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(max_df=700, ngram_range=(1,2))),
    ('nb_clf', MultinomialNB())
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/naver_tfidf_nb.pkl')
print('Case 4. TfidfVectorizer + NaiveBayes done.')
