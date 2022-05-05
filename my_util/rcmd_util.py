import numpy as np
import pandas as pd
import warnings, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings('ignore')
cosine_sim_loaded = False
cosine_sim = np.array([])
df = pd.DataFrame()

def get_cosine_sim():
    global cosine_sim, cosine_sim_loaded, df
    if cosine_sim_loaded:
        return

    df = pd.read_csv('static/data/movies_summary.csv')
    df.dropna(how='any', inplace=True)
    df = df.head(10000)
    df['total'] = df.overview + ' ' + df.director + ' ' + df.cast3

    tvect = TfidfVectorizer(stop_words='english')
    dtm = tvect.fit_transform(df.total)
    cosine_sim = linear_kernel(dtm, dtm)
    cosine_sim_loaded = True

def get_original_name(s):
    capital = re.findall('[A-Z]', s)
    small = re.split('[A-Z]', s)[1:]
    name = ' '.join([x+y for x, y in zip(capital, small)])
    return name

def get_recommendations(index):
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_list = []
    for i in sim_scores:
        title = df.title.iloc[i[0]]
        overview = df.overview.iloc[i[0]]
        director = get_original_name(df.director.iloc[i[0]])
        casts = df.cast3.iloc[i[0]]
        casts = ', '.join(map(get_original_name, casts.split()))
        movie_list.append({'title':title, 'overview':overview, 'director':director, 'casts':casts})
    title = df.title[index]
    overview = df.overview[index]
    director = get_original_name(df.director[index])
    casts = df.cast3[index]
    casts = ', '.join(map(get_original_name, casts.split()))
    title_dict = {'title':title, 'overview':overview, 'director':director, 'casts':casts}
    return movie_list, title_dict

''' def get_cosine_sim():
    global cosine_sim, cosine_sim_loaded, df
    if cosine_sim_loaded:
        return
    df = pd.read_csv('static/data/movies_meta_summary.csv')

    tvect = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tvect.fit_transform(df.overview)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim_loaded = True

def get_recommendations(index):
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_list = [df.title.iloc[i[0]] for i in sim_scores]
    title = df.title[index]
    return movie_list, title '''

def get_movie_index(title):
    indices = pd.Series(df.index, index=df.title)
    try:
        index = indices[title]
    except:
        index = -1
    return index

def get_recommended_books(index):
    df = pd.read_csv('static/data/books2.csv')
    tvect = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tvect.fit_transform(df.cleaned)
    book_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    sim_scores = list(enumerate(book_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:6]
    book_indices = [i[0] for i in sim_scores]
    return book_indices

def get_book_index(title):
    df = pd.read_csv('static/data/books2.csv')
    title_len = len(title)
    for i in df.index:
        if title.lower() == df.title[i].lower()[:title_len]:
            return i
    return -1
