from flask import Blueprint, render_template, request, session, g
from flask import current_app, redirect, url_for
from sklearn.datasets import load_digits
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import ResNet50, decode_predictions
from PIL import Image, ImageDraw, ImageFont
import os, joblib
import requests, urllib3, json, base64
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import my_util.general_util as gu
import my_util.advanced_util as au
from my_util.weather import get_weather

aclsf_bp = Blueprint('aclsf_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':1, 're':0, 'cu':0, 'nl':0, 'st':0}

digits_max_index = 445
mnist_max_index = 10487
fashion_mnist_max_index = 9995
news_max_index = 4438
max_image_size = 2048
max_image_len = 2 ** 21

@aclsf_bp.before_app_first_request
def before_app_first_request():
    global resnet
    resnet = ResNet50()
    logging.debug('===== Advanced Blueprint before_app_first_request() =====') 
    #global imdb_count_lr, imdb_tfidf_lr
    #global naver_count_lr, naver_count_nb, naver_tfidf_lr, naver_tfidf_nb
    #global news_count_lr, news_tfidf_lr, news_tfidf_sv
    #imdb_count_lr = joblib.load('static/model/imdb_count_lr.pkl')
    #imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl')
    #naver_count_lr = joblib.load('static/model/naver_count_lr.pkl')
    #naver_count_nb = joblib.load('static/model/naver_count_nb.pkl')
    #naver_tfidf_lr = joblib.load('static/model/naver_tfidf_lr.pkl')
    #naver_tfidf_nb = joblib.load('static/model/naver_tfidf_nb.pkl')
    #news_count_lr = joblib.load('static/model/news_count_lr.pkl')
    #news_tfidf_lr = joblib.load('static/model/news_tfidf_lr.pkl')
    #news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl')

@aclsf_bp.route('/digits', methods=['GET', 'POST'])
def digits():
    if request.method == 'GET':
        return render_template('advanced/digits.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], digits_max_index)
        #index = int(request.form['index'] or '0')
        index_list = list(range(index, index+5))
        digits = load_digits()
        df = pd.read_csv('static/data/digits_test.csv')
        img_index_list = df['index'].values
        target_index_list = df['target'].values
        index_list = img_index_list[index:index+5]

        scaler = joblib.load('static/model/digits_scaler.pkl')
        test_data = df.iloc[index:index+5, 1:-1]
        test_scaled = scaler.transform(test_data)
        label_list = target_index_list[index:index+5]
        lrc = joblib.load('static/model/digits_lr.pkl')
        svc = joblib.load('static/model/digits_sv.pkl')
        rfc = joblib.load('static/model/digits_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/digit')
        for k, i in enumerate(index_list):
            plt.figure(figsize=(2,2))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(k+1) + '.png'
            plt.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list,
                       'pred_lr':pred_lr, 'pred_sv':pred_sv, 'pred_rf':pred_rf}
        
        return render_template('advanced/digits_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@aclsf_bp.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'GET':
        return render_template('advanced/mnist.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], mnist_max_index)
        #index = int(request.form['index'] or '0')
        index_list = list(range(index, index+3))
        df = pd.read_csv('static/data/mnist/mnist_test.csv')

        scaler = joblib.load('static/model/mnist_scaler.pkl')
        test_data = df.iloc[index:index+3, 1:-1].values
        test_scaled = scaler.transform(test_data)
        label_list = df.iloc[index:index+3, -1]
        svc = joblib.load('static/model/mnist_sv.pkl')
        pred_sv = svc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/mnist')
        for i in range(3):
            digit = test_data[i].reshape(28,28)
            plt.figure(figsize=(4,4))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(i+1) + '.png'
            plt.imshow(digit, cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list, 'pred_sv':pred_sv}
        
        return render_template('advanced/mnist_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@aclsf_bp.route('/fmnist', methods=['GET', 'POST'])
def fmnist():
    if request.method == 'GET':
        return render_template('advanced/fashion_mnist.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], fashion_mnist_max_index)
        index_list = list(range(index, index+5))
        (_, _), (X_test, y_test) = fashion_mnist.load_data()
        test_data = X_test[index:index+5]
        test_data = test_data.reshape(-1, 28, 28, 1) / 255.
        model = load_model('static/model/fashion_mnist_cnn.h5')
        pred = model.predict(test_data)
        result = np.argmax(pred, axis=1)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/fashion')
        for k, i in enumerate(index_list):
            plt.figure(figsize=(2,2))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(k+1) + '.png'
            plt.imshow(X_test[i], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        result_dict = {'index':index_list, 'label':y_test[index:index+5], 'pred_cnn':result}
        return render_template('advanced/fashion_mnist_res.html', menu=menu, mtime=mtime,
                                result=result_dict, cn=class_names, weather=get_weather())


@aclsf_bp.route('/news', methods=['GET', 'POST'])
def news():
    target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
                    'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
                    'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
                    'sci.space', 'soc.religion.christian', 'talk.politics.guns',
                    'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']
    if request.method == 'GET':
        return render_template('advanced/news.html', menu=menu, weather=get_weather())
    else:
        index = gu.get_index(request.form['index'], news_max_index)
        df = pd.read_csv('static/data/news/test.csv')
        label = f'{df.target[index]} ({target_names[df.target[index]]})'
        test_data = []
        test_data.append(df.data[index])

        news_count_sv = joblib.load('static/model/news_count_sv.pkl')
        news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl')
        pred_c_sv = news_count_sv.predict(test_data)
        pred_t_sv = news_tfidf_sv.predict(test_data)
        result_dict = {'index':index, 'label':label, 
                       'pred_c_sv':f'{pred_c_sv[0]} ({target_names[pred_c_sv[0]]})',
                       'pred_t_sv':f'{pred_t_sv[0]} ({target_names[pred_t_sv[0]]})'}
        
        return render_template('advanced/news_res.html', menu=menu, news=df.data[index],
                                res=result_dict, weather=get_weather())

@aclsf_bp.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'GET':
        return render_template('advanced/image.html', menu=menu, weather=get_weather())
    else:
        f_img = request.files['image']
        file_img = os.path.join(current_app.root_path, 'static/upload/') + f_img.filename
        f_img.save(file_img)
        current_app.logger.debug(f"{f_img.filename}, {file_img}")

        #img = np.array(Image.open(file_img).resize((224, 224)))
        img = au.center_image(Image.open(file_img), return_format='Array')
        yhat = resnet.predict(img.reshape(-1, 224, 224, 3))
        label = decode_predictions(yhat)
        label = label[0][0]
        mtime = int(os.stat(file_img).st_mtime)
        return render_template('advanced/image_res.html', menu=menu, weather=get_weather(),
                               name=label[1], prob=np.round(label[2]*100, 2),
                               filename=f_img.filename, mtime=mtime)    

# 카카오 비전 Open API - 얼굴 검출
@aclsf_bp.route('/face', methods=['GET', 'POST'])
def face():
    if request.method == 'GET':
        return render_template('advanced/face.html', menu=menu, weather=get_weather())
    else:
        f_img = request.files['image']
        file_img = os.path.join(current_app.root_path, 'static/upload/') + f_img.filename
        f_img.save(file_img)
        _, image_type = os.path.splitext(f_img.filename)
        if image_type[1:] not in ['png', 'jpg']:
            return redirect(url_for('aclsf_bp.face'))
        img = Image.open(file_img)
        if sum(img.size) > max_image_size or len(img.tobytes()) > max_image_len:
            return redirect(url_for('aclsf_bp.face'))
        current_app.logger.debug(f"{f_img.filename}, {image_type}, {img.size}")
        
        with open('static/keys/kakaoaikey.txt') as file:
            kakao_key = file.read()
        url = 'https://dapi.kakao.com/v2/vision/face/detect'
        headers = {"Authorization": f'KakaoAK {kakao_key}'}
        files = {'image': open(file_img, 'rb')}
        result = requests.post(url, headers=headers, files=files)
        if result.status_code != 200:
            return redirect(url_for('aclsf_bp.face'))
            
        res = result.json()
        faces = res['result']['faces']
        width, height = img.size
        draw = ImageDraw.Draw(img)
        for i in range(len(faces)):
            face = faces[i]
            x = int(face['x']*width)
            w = int(face['w']*width)
            y = int(face['y']*height)
            h = int(face['h']*height)
            draw.rectangle(((x, y), (x+w, y+h)), outline='green', width=2)
            text = '남' if face['facial_attributes']['gender']['male'] > 0.5 else '여'
            text += str(int(float(faces[i]['facial_attributes']['age']+0.5)))
            draw.text((x+10, y-20), text, font=ImageFont.truetype('NanumGothic.ttf', 20), fill=(0,255,0))
            for key in face['facial_points'].keys():
                for part in face['facial_points'][key]:
                    x = int(float(part[0]) * width)
                    y = int(float(part[1]) * height)
                    draw.ellipse((x-2, y-2, x+2, y+2), fill='white', outline='white')
        
        face_img = os.path.join(current_app.root_path, 'static/img/face'+image_type)
        img.save(face_img)
        mtime = int(os.stat(face_img).st_mtime)
        return render_template('advanced/face_res.html', menu=menu, weather=get_weather(),
                               filename='face'+image_type, mtime=mtime)

# 카카오 비전 Open API - 문자 인식(OCR)
@aclsf_bp.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if request.method == 'GET':
        return render_template('advanced/ocr.html', menu=menu, weather=get_weather())
    else:
        f_img = request.files['image']
        file_img = os.path.join(current_app.root_path, 'static/upload/') + f_img.filename
        f_img.save(file_img)
        _, image_type = os.path.splitext(f_img.filename)
        img = Image.open(file_img)
        current_app.logger.debug(f"{f_img.filename}, {image_type}, {img.size}")
        
        with open('static/keys/kakaoaikey.txt') as file:
            kakao_key = file.read()
        url = 'https://dapi.kakao.com/v2/vision/text/ocr'
        headers = {"Authorization": f'KakaoAK {kakao_key}'}
        files = {'image': open(file_img, 'rb')}
        result = requests.post(url, headers=headers, files=files)
        if result.status_code != 200:
            return redirect(url_for('aclsf_bp.ocr'))
            
        res = result.json()
        texts = []
        draw = ImageDraw.Draw(img)
        for obj in res['result']:
            try:
                draw.rectangle((tuple(obj['boxes'][0]), tuple(obj['boxes'][2])), outline='green', width=3)
            except:
                draw.rectangle((tuple(obj['boxes'][0]), tuple(obj['boxes'][2])), width=5)
            texts.append(obj['recognition_words'][0])
        
        ocr_img = os.path.join(current_app.root_path, 'static/img/ocr'+image_type)
        img.save(ocr_img)
        mtime = int(os.stat(ocr_img).st_mtime)
        return render_template('advanced/ocr_res.html', menu=menu, weather=get_weather(),
                               texts=', '.join(texts), filename='ocr'+image_type, mtime=mtime)

# 국내 서버에서는 이용가능하나 해외 서버에서는 사용 불가
@aclsf_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'GET':
        return render_template('advanced/detect.html', menu=menu, weather=get_weather())
    else:
        f_img = request.files['image']
        file_img = os.path.join(current_app.root_path, 'static/upload/') + f_img.filename
        f_img.save(file_img)
        _, image_type = os.path.splitext(f_img.filename)
        image_type = 'jpg' if image_type == '.jfif' else image_type[1:]
        current_app.logger.debug(f"{f_img.filename}, {image_type}")

        # 공공 인공지능 Open API - 객체 검출
        with open('static/keys/etri_ai_key.txt') as kfile:
            eai_key = kfile.read()
        with open(file_img, 'rb') as file:
            image_contents = base64.b64encode(file.read()).decode('utf8')
        openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
        request_json = {
            "request_id": "reserved field",
            "access_key": eai_key,
            "argument": {
                "file": image_contents,
                "type": image_type
            }
        }
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json)
        )
        if response.status != 200:
            return redirect(url_for('aclsf_bp.detect'))

        result_json = json.loads(response.data)
        obj_list = result_json['return_object']['data']
        image = Image.open(file_img)
        draw = ImageDraw.Draw(image)
        object_list = []
        for obj in obj_list:
            name = obj['class']
            x = int(obj['x'])
            y = int(obj['y'])
            w = int(obj['width'])
            h = int(obj['height'])
            draw.text((x+10,y+10), name, font=ImageFont.truetype('NanumGothic.ttf', 20), fill=(255,0,0))
            draw.rectangle(((x, y), (x+w, y+h)), outline=(255,0,0), width=2)
            object_list.append(name)
        object_img = os.path.join(current_app.root_path, 'static/img/object.'+image_type)
        image.save(object_img)
        mtime = int(os.stat(object_img).st_mtime)
        return render_template('advanced/detect_res.html', menu=menu, weather=get_weather(),
                               object_list=', '.join(obj for obj in object_list),
                               filename='object.'+image_type, mtime=mtime) 
