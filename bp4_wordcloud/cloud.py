from flask import Blueprint, render_template, request
from flask import current_app
import os, logging
from my_util.weather import get_weather
from my_util.wordCloud import engCloud, hanCloud

cloud_bp = Blueprint('cloud_bp', __name__)
menu = {'ho':0, 'bb':0, 'ma':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':1, 'rs':0,
        'cf':0, 'ac':0, 'rc':0, 'nl':0, 'st':0, 'mi':0}

@cloud_bp.route('/han/gift')
def gift():
    textfile = os.path.join(current_app.static_folder, 'data/gift.txt')
    maskfile = os.path.join(current_app.static_folder, 'img/heart.jpg')
    logging.debug(f'{textfile}, {maskfile}')
    stoptext = """
        선물 추천 것 가격 수 기능 제품 저 제 생각 여자 여자친구 사용 요 더 구매 고급 주문
        판매 때 참고 머리 하나 해 한번 제작 용 준 디자인 거 네이버 사람 배송 중 후기 감동
        하트 여친 커플 가능 사랑 인기 상품 직접 브랜드 선택 곳 모양 마감 요즘 노늘 가지 남녀
        그냥 위 페이 마음 부담 오늘 남자 협찬 전 핸드 의미 도움 색상 아래 포장 처 조금 하루 정도
        확인 채택 수수료 정액 답변 스 이 제공 정말 파트너 생일 변경 지금 활동 쿠팡 통해 각인
    """
    stop_words = stoptext.split()
    img_file = os.path.join(current_app.static_folder, 'tmp/text.png')
    with open(textfile, encoding='utf-8') as fp:
        text = fp.read()
    hanCloud(text, stop_words, maskfile, img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                            filename='gift.txt', mtime=mtime)

@cloud_bp.route('/eng/<option>')
def eng(option):
    if option == 'Alice':
        filename = 'Alice.txt'
        maskfile = os.path.join(current_app.static_folder, 'img/Alice_mask.png')
        stop_words = ['said']
    else:
        filename = 'A_new_hope.txt'
        maskfile = os.path.join(current_app.static_folder, 'img/Stormtrooper_mask.png')
        stop_words = ['int', 'ext']
    
    textfile = os.path.join(current_app.static_folder, 'data/') + filename
    logging.debug(f'{textfile}, {maskfile}')
    img_file = os.path.join(current_app.static_folder, 'tmp/text.png')
    with open(textfile) as fp:
        text = fp.read()
    if option == 'Starwars':
        text = text.replace('HAN', 'Han')
        text = text.replace("LUKE'S", 'Luke')
    engCloud(text, stop_words, maskfile, img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                            filename=filename, mtime=mtime)        

@cloud_bp.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'GET':
        return render_template('wordcloud/text.html', menu=menu, weather=get_weather())
    else:
        lang = request.form['lang']
        f_text = request.files['text']
        file_text = os.path.join(current_app.static_folder, 'upload/') + f_text.filename
        f_text.save(file_text)
        if request.files['mask']:
            f_mask = request.files['mask']
            file_mask = os.path.join(current_app.static_folder, 'upload/') + f_mask.filename
            f_mask.save(file_mask)
        else:
            file_mask = None
        stop_words = request.form['stop_words']
        current_app.logger.debug(f"{lang}, {f_text}, {request.files['mask']}, {stop_words}")

        text = open(file_text, encoding='utf-8').read()
        stop_words = stop_words.split(' ') if stop_words else []
        img_file = os.path.join(current_app.static_folder, 'tmp/text.png')
        if lang == 'en':
            engCloud(text, stop_words, file_mask, img_file)
        else:
            hanCloud(text, stop_words, file_mask, img_file)

        mtime = int(os.stat(img_file).st_mtime)
        return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                                filename=f_text.filename, mtime=mtime)
