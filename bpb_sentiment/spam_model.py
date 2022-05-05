# Spam 메일 분류
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('../static/data/spam_전처리완료.csv')
df['clean'] = df.v2.str.replace('[^A-Za-z0-9]',' ').str.strip().str.lower()
X_train, X_test, y_train, y_test = train_test_split(
    df.clean, df.v1, stratify=df.v1, test_size=0.25, random_state=2022
)

df_test = pd.DataFrame(df.v2[X_test.index].values, columns=['content'])
df_test['label'] = y_test.values
df_test.to_csv('../static/data/spam_test.csv', index=False)

# Case 1. CountVectorizer + NaiveBayes
pipeline1 = Pipeline([ 
    ('cvect', CountVectorizer(stop_words='english', max_df=0.9, ngram_range=(1,2))),
    ('nb', MultinomialNB())
])
pipeline1.fit(X_train, y_train)
joblib.dump(pipeline1, '../static/model/spam_count_nb.pkl')

# Case 2. TfidfVectorizer + LogisticRegression
pipeline2 = Pipeline([ 
    ('tvect', TfidfVectorizer(stop_words='english', max_df=0.9, ngram_range=(1,2))),
    ('lr', LogisticRegression(C=10, random_state=2022))
])
pipeline2.fit(X_train, y_train)
joblib.dump(pipeline2, '../static/model/spam_tfidf_lr.pkl')
