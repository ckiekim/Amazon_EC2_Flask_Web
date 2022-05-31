import re, joblib
import numpy as np
import pandas as pd
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, GRU, Dense, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

seed = 2022
np.random.seed(seed)
tf.random.set_seed(seed)

url = 'https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt'
df = pd.read_table(url, names=['ratings','reviews'])
df['label'] = df.ratings.apply(lambda x: 1 if x >= 4 else 0)
df.drop_duplicates(subset=['reviews'], inplace=True)
df.reviews = df.reviews.str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '')

X_train, X_test, y_train, y_test = train_test_split(
    df.reviews.values, df.label.values, stratify=df.label.values,
    test_size=0.2, random_state=seed
)

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을','ㅋㅋ','ㅠㅠ','ㅎㅎ']
okt = Okt()
train_data = []
for sentence in X_train:
    morphs = okt.morphs(sentence, stem=True)
    tmp_X = [word for word in morphs if word not in stopwords]
    train_data.append(tmp_X)
print('train data done')
dtf = pd.DataFrame({'reviews':X_test, 'label':y_test})
dtf.to_csv('../static/data/shopping_test.csv', index=False)

t = Tokenizer()
t.fit_on_texts(train_data)
threshold = 3
total_cnt = len(t.word_index)   
rare_cnt, total_freq, rare_freq = 0, 0, 0
for key, value in t.word_counts.items():
    total_freq += value
    if value < threshold:
        rare_cnt += 1
        rare_freq += value
print('단어 집합(vocabulary)의 크기 :', total_cnt)
print(f'등장 빈도가 {threshold - 1}번 이하인 희귀 단어의 수: {rare_cnt}')
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)
vocab_size = total_cnt - rare_cnt + 2

t = Tokenizer(num_words=vocab_size, oov_token='OOV')
t.fit_on_texts(train_data)
joblib.dump(t, '../static/model/shopping_tokenizer.pkl')
X_train = t.texts_to_sequences(train_data)
max_len = 60
X_train = pad_sequences(X_train, maxlen=max_len)

model = Sequential([ 
    Embedding(vocab_size, 100, input_length=max_len),
    LSTM(128),
    Dense(1, activation='sigmoid')
])
model.compile('adam', 'binary_crossentropy', ['accuracy'])
model_path = '../static/model/shopping_lstm.h5'
mc = ModelCheckpoint(model_path, verbose=1, save_best_only=True)
es = EarlyStopping(patience=3)
hist = model.fit(
    X_train, y_train, validation_split=0.2, verbose=0,
    epochs=30, batch_size=128, callbacks=[mc, es]
)
best_model = load_model(model_path)

