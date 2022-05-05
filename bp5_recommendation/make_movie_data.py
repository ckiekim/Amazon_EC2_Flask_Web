import pandas as pd
from ast import literal_eval
import warnings, re
warnings.filterwarnings('ignore')

def get_3cast(x):
    cast = []
    for item in x:
        if item['name'] not in cast:
            cast.append(item['name'])
    cast = list(map(lambda s: re.sub(' ', '', s), cast))
    cast = cast if len(cast) <= 3 else cast[:3]
    return ' '.join(cast)

def get_director(x):
    for item in x:
        if item['job'] == 'Director':
            return item['name'].replace(' ', '')
    return ''

movie = pd.read_csv('../static/data/movies/movies_metadata.csv', low_memory=False)
info = pd.read_csv('../static/data/movies/credits.csv')

df = movie[['id','title','overview']]
df.dropna(how='any', inplace=True)
df.drop_duplicates(subset=['title'], inplace=True)
df.id = df.id.astype(int)
info.id = info.id.astype(int)
df = pd.merge(df, info)

df.cast = df.cast.apply(literal_eval)
print('Cast extraction done.')
df['cast3'] = df.cast.apply(get_3cast)
df.crew = df.crew.apply(literal_eval)
print('Director extraction done.')
df['director'] = df.crew.apply(get_director)
df.drop(columns=['cast','crew'], inplace=True)
df.to_csv('../static/data/movies_summary.csv', index=False)
