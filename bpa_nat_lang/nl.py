from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for
import os, json, requests, re, joblib
from urllib.parse import quote
#from konlpy.tag import Okt
from my_util.global_vars import okt
from my_util.weather import get_weather

nl_bp = Blueprint('nl_bp', __name__)
menu = {'ho':0, 'bb':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':1, 'st':0}

@nl_bp.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return render_template('nat_lang/translate.html', menu=menu, weather=get_weather())
    else:
        text = request.form['text']
        lang = request.form['lang']

        # 카카오 번역기
        with open('static/keys/kakaoaikey.txt') as kfile:
            kai_key = kfile.read()
        text = text.replace('\n',' ').replace('\r','')
        k_url = f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang=kr&target_lang={lang}'
        result = requests.get(k_url,
                              headers={"Authorization": "KakaoAK "+kai_key}).json()
        tr_text_list = result['translated_text'][0]
        k_translated_text = '\n'.join([tmp_text for tmp_text in tr_text_list])

        return render_template('nat_lang/translate_res.html', menu=menu, weather=get_weather(),
                                org=text, kakao=k_translated_text, lang=lang)

@nl_bp.route('/tts', methods=['GET', 'POST'])
def tts():
    if request.method == 'GET':
        return render_template('nat_lang/tts.html', menu=menu, weather=get_weather())
    else:
        text = request.form['text']

        # 카카오 음성합성 - 음성 활성화 설정을 ON 해야함
        with open('static/keys/kakaoaikey.txt') as kfile:
            kai_key = kfile.read()
        data = f'<speak>{text}</speak>'
        t_url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize'
        headers={"Content-Type": "application/xml",
                "Authorization": "KakaoAK " + kai_key}
        response = requests.post(t_url, data=data.encode('utf-8'), headers=headers)
        rescode = response.status_code
        audio_file = os.path.join(current_app.root_path, 'static/img/tts.mp3')
        if rescode == 200:
            with open(audio_file, 'wb') as f:
                f.write(response.content)
        mtime = int(os.stat(audio_file).st_mtime)

        return render_template('nat_lang/tts_res.html', menu=menu, weather=get_weather(),
                                text=text, mtime=mtime)


@nl_bp.route('/emotion', methods=['GET', 'POST'])
def emotion():
    if request.method == 'GET':
        return render_template('nat_lang/emotion.html', menu=menu, weather=get_weather())
    else:
        text = request.form['text']

        # 카카오 언어감지
        with open('static/keys/kakaoaikey.txt') as kfile:
            kai_key = kfile.read(100)
        k_url = f'https://dapi.kakao.com/v3/translation/language/detect?query={quote(text)}'
        result = requests.get(k_url,
                              headers={"Authorization": "KakaoAK "+kai_key}).json()
        lang = result['language_info'][0]['code']

        # 카카오 번역기
        if lang == 'kr':
            k_url = f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang=kr&target_lang=en'
        else:
            k_url = f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang=en&target_lang=kr'
        result = requests.get(k_url,
                              headers={"Authorization": "KakaoAK "+kai_key}).json()
        tr_text_list = result['translated_text'][0]
        tr_text = '\n'.join([tmp_text for tmp_text in tr_text_list])

        #okt = Okt()
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
        if lang == 'kr':
            review = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
        else:
            review = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", tr_text)
        morphs = okt.morphs(review, stem=True) # 토큰화
        ko_review = ' '.join([word for word in morphs if not word in stopwords]) # 불용어 제거
        en_review = tr_text if lang == 'kr' else text

        naver_tfidf_nb = joblib.load('static/model/naver_tfidf_nb.pkl')
        imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl')
        pred_ko = '긍정' if naver_tfidf_nb.predict([ko_review])[0] else '부정'
        pred_en = '긍정' if imdb_tfidf_lr.predict([en_review])[0] else '부정'

        if lang == 'kr':
            res = {'src_text':text, 'dst_text':tr_text, 'src_pred':pred_ko, 'dst_pred':pred_en}
        else:
            res = {'src_text':text, 'dst_text':tr_text, 'src_pred':pred_en, 'dst_pred':pred_ko}

        return render_template('nat_lang/emotion_res.html', res=res,
                                menu=menu, weather=get_weather())
