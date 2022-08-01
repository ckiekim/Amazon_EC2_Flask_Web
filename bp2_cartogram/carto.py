from flask import Blueprint, render_template, request
from flask import current_app
import os
import pandas as pd
from my_util.weather import get_weather
import my_util.drawKorea as dk

carto_bp = Blueprint('carto_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':1, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':0, 'mi':0}

@carto_bp.route('/pop/<option>')
def population(option):
    df_pop = pd.read_csv('./static/data/population.csv')
    column_dict = {'crisis_area':'소멸위기지역', 'crisis_ratio':'소멸비율', 'high_crisis':'소멸위기고위험지역'}
    color_dict = {'crisis_area':'Reds', 'crisis_ratio':'Oranges', 'high_crisis':'Purples'}
    img_file = os.path.join(current_app.root_path, 'static/tmp/population.png')
    dk.drawKorea(column_dict[option], df_pop, color_dict[option], img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('cartogram/population.html', menu=menu, weather=get_weather(),
                            option=option, column_dict=column_dict, mtime=mtime)

@carto_bp.route('/coffee', methods=['GET', 'POST'])
def coffee():
    if request.method == 'GET':
        return render_template('cartogram/coffee.html', menu=menu, weather=get_weather())
    else:
        item = request.form['item']
        coffee_index = pd.read_csv('./static/data/커피지수.csv', 
                                   dtype={'이디야':int, '스타벅스':int, '커피빈':int, '빽다방':int})

        color_dict = {'커피지수':'Reds', '이디야':'Blues', '스타벅스':'Greens', '커피빈':'PuBu', '빽다방':'Oranges'}
        img_file = os.path.join(current_app.root_path, 'static/tmp/coffee.png')
        dk.drawKorea(item, coffee_index, color_dict[item], img_file)
        mtime = int(os.stat(img_file).st_mtime)

        df = coffee_index.sort_values(by=item, ascending=False)[['ID',item]].reset_index()
        top10 = {}
        for i in range(10):
            top10[df['ID'][i]] = round(df[item][i], 2)
        return render_template('cartogram/coffee_res.html', menu=menu, weather=get_weather(),
                               item=item, mtime=mtime, top10=top10)
