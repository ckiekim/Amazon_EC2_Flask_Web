import pandas as pd
import warnings, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings('ignore')
df = pd.read_csv('../static/data/movies_meta_summary.csv')
df = df.head(20000)
tvect = TfidfVectorizer(stop_words='english')
tfidf_matrix = tvect.fit_transform(df.overview)
indices = pd.Series(df.index, index=df.title).drop_duplicates()

print('Starting ...')
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print('similarity')
joblib.dump(cosine_sim, '../static/data/movie_cos_sim.pkl')
