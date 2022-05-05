from flask import Blueprint, render_template, request, session, g
from flask import current_app
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import my_util.general_util as gu
from my_util.weather import get_weather

rgrs_bp = Blueprint('rgrs_bp', __name__)
menu = {'ho':0, 'bb':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':1, 'cu':0, 'nl':0, 'st':0}

diabetes_max_index = 110
iris_max_index = 37
boston_max_index = 126

@rgrs_bp.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'GET':
        return render_template('regression/diabetes.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], diabetes_max_index)
        #index = int(request.form['index'] or '0')
        feature = request.form['feature']
        df = pd.read_csv('static/data/diabetes_train.csv')
        X = df[feature].values.reshape(-1,1)
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/diabetes_test.csv')
        X_test = df_test[feature][index]
        y_test = df_test.target[index]
        pred = np.round(X_test * weight[0] + bias, 2)

        y_min = np.min(X) * weight[0] + bias
        y_max = np.max(X) * weight[0] + bias
        plt.figure()
        plt.scatter(X, y, label='train')
        plt.plot([np.min(X), np.max(X)], [y_min, y_max], 'r', lw=3)
        plt.scatter([X_test], [y_test], c='r', marker='*', s=100, label='test')
        plt.grid()
        plt.legend()
        plt.title(f'Diabetes target vs. {feature}')
        img_file = os.path.join(current_app.root_path, 'static/img/diabetes.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index, 'feature':feature, 'y':y_test, 'pred':pred}
        return render_template('regression/diabetes_res.html', res=result_dict, mtime=mtime,
                                menu=menu, weather=get_weather())

@rgrs_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('regression/iris.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], iris_max_index)
        #index = int(request.form['index'] or '0')
        feature_name = request.form['feature']
        column_dict = {'sl':'Sepal length', 'sw':'Sepal width', 
                       'pl':'Petal length', 'pw':'Petal width', 
                       'species':['Setosa', 'Versicolor', 'Virginica']}
        column_list = list(column_dict.keys())

        df = pd.read_csv('static/data/iris_train.csv')
        df.columns = column_list
        X = df.drop(columns=feature_name, axis=1).values
        y = df[feature_name].values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/iris_test.csv')
        df_test.columns = column_list
        X_test = df_test.drop(columns=feature_name, axis=1).values[index]
        pred_value = np.dot(X_test, weight.T) + bias

        x_test = list(df_test.iloc[index,:-1].values)
        x_test.append(column_dict['species'][int(df_test.iloc[index,-1])])
        org = dict(zip(column_list, x_test))
        pred = dict(zip(column_list[:-1], [0,0,0,0]))
        pred[feature_name] = np.round(pred_value, 2)
        return render_template('regression/iris_res.html', menu=menu, weather=get_weather(),
                                index=index, org=org, pred=pred, feature=column_dict[feature_name])

@rgrs_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    if request.method == 'GET':
        feature_list = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
                        'TAX', 'PTRATIO', 'B', 'LSTAT']
        return render_template('regression/boston.html', feature_list=feature_list,
                               menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], boston_max_index)
        #index = int(request.form['index'] or '0')
        feature_list = request.form.getlist('feature')
        if len(feature_list) == 0:
            feature_list = ['RM', 'LSTAT']
        df = pd.read_csv('static/data/boston_train.csv')
        X = df[feature_list].values
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/boston_test.csv')
        X_test = df_test[feature_list].values[index, :]
        y_test = df_test.target[index]
        pred = np.dot(X_test, weight.T) + bias      # tmp = lr.predict(X_test.reshape(1,-1))
        pred = np.round(pred, 2)                    # pred = np.round(tmp[0])

        result_dict = {'index':index, 'feature':feature_list, 'y':y_test, 'pred':pred}
        org = dict(zip(df.columns[:-1], df_test.iloc[index, :-1]))
        return render_template('regression/boston_res.html', res=result_dict, org=org,
                               menu=menu, weather=get_weather())
