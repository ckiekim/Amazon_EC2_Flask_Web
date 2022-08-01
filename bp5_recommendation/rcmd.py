from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
import joblib
import pandas as pd
import my_util.rcmd_util as mr
import my_util.general_util as gu
from my_util.weather import get_weather

rcmd_bp = Blueprint('rcmd_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':1,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':0, 'mi':0}

movie_max_index = 7999      # AWS EC2 8000, Oracle cloud 10000
book_max_index = 2380
ml_latest_max_index = 610
ml_latest_min_index = 1

@rcmd_bp.route('/movie', methods=['GET', 'POST'])
def movie():
    if request.method == 'GET':
        return render_template('rcmd/spinner.html', menu=menu, weather=get_weather())
    else:
        mr.get_cosine_sim()
        df = pd.read_csv('static/data/movies_meta_summary.csv')
        
        movie_dict = dict(zip(df.title, df.index))
        return render_template('rcmd/movie.html', menu=menu, weather=get_weather(),
                                movie_dict=movie_dict)

@rcmd_bp.route('/movie_res', methods=['POST'])
def movie_res():
    kind = request.form['kind']
    if kind == 'list':
        index = int(request.form['list'])
    elif kind == 'index':
        index = gu.get_index(request.form['index'], movie_max_index)
        #index = int(request.form['index'] or '0')
    else:
        title = request.form['title']
        index = mr.get_movie_index(title)
        if index < 0:
            flash('입력한 영화제목 데이터가 없습니다.')
            return redirect(url_for('rcmd_bp.movie'))

    movie_list, my_dict = mr.get_recommendations(index)
    return render_template('rcmd/movie_res.html', menu=menu, weather=get_weather(),
                            movie_list=movie_list, my_dict=my_dict)

@rcmd_bp.route('/book', methods=['GET', 'POST'])
def book():
    df = pd.read_csv('static/data/books2.csv')
    if request.method == 'GET':
        book_dict = dict(zip(df.title, df.index))
        return render_template('rcmd/book.html', menu=menu, weather=get_weather(),
                                book_dict=book_dict)
    else:
        kind = request.form['kind']
        if kind == 'list':
            index = int(request.form['list'])
        elif kind == 'index':
            index = gu.get_index(request.form['index'], book_max_index)
            #index = int(request.form['index'] or '0')
        else:
            title = request.form['title']
            index = mr.get_book_index(title)
            if index < 0:
                flash('입력한 도서제목 데이터가 없습니다.')
                return redirect(url_for('rcmd_bp.book'))
    
    book_indices = mr.get_recommended_books(index)
    book_list = []
    for i in book_indices:
        book_list.append([df.image_link[i], df.title[i], df.author[i], df.genre[i]])
    return render_template('rcmd/book_res.html', menu=menu, weather=get_weather(),
                            book_list=book_list)

def sortkey_est(pred):
    return pred.est

@rcmd_bp.route('/ml_latest', methods=['GET', 'POST'])
def ml_latest():
    if request.method == 'GET':
        return render_template('rcmd/ml_latest.html', menu=menu, weather=get_weather())
    else:
        rdf = pd.read_csv('static/data/ml-latest/ratings.csv')
        mdf = pd.read_csv('static/data/ml-latest/movies.csv')
        model = joblib.load('static/model/movie-surprise.pkl')
        uid = gu.get_index(request.form['index'], ml_latest_max_index, ml_latest_min_index)
        seen_movies = rdf[rdf.userId == uid]['movieId'].tolist()
        total_movies = mdf.movieId.tolist()
        unseen_movies = [movie for movie in total_movies if movie not in seen_movies]
        predictions = [model.predict(str(uid), str(mid)) for mid in unseen_movies]
        predictions.sort(key=sortkey_est, reverse=True)
        rcmd_list = []
        for pred in predictions[:10]:
            mid = int(pred.iid)
            rating = round(pred.est, 4)
            title = mdf[mdf.movieId == mid]['title'].values[0]
            genre = mdf[mdf.movieId == mid]['genres'].values[0]
            genre = ', '.join(genre.split('|'))
            rcmd_list.append({'id':mid, 'title':title, 'genre':genre, 'rating':rating})
        return render_template('rcmd/ml_latest_res.html', menu=menu, weather=get_weather(),
                                uid=uid, movie_list=rcmd_list)
