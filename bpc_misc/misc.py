from flask import Blueprint, render_template, request, session, g
from flask import current_app, flash, redirect
import os, random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from my_util.weather import get_weather

misc_bp = Blueprint('misc_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':0, 'mi':1}


@misc_bp.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        return render_template('misc/order.html', menu=menu, weather=get_weather())
    else:
        num = int(request.form['number'])
        if num <= 1 or num >= 10:
            flash('2에서 9사이의 숫자를 입력하세요.')
            return redirect('/misc/order')
        teams = [i for i in range(1, num+1)]
        random.seed(datetime.now().microsecond)
        finals = random.sample(teams, num)
        return render_template('misc/order_res.html', menu=menu, finals=finals, weather=get_weather())
