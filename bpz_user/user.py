from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
import logging, math, hashlib, base64
import db.db_module as dm
from my_util.weather import get_weather

user_bp = Blueprint('user_bp', __name__)
menu = {'ho':0, 'bb':0, 'us':1, 'li':0, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@user_bp.route('/list/<int:page>', methods=['GET'])
def list(page):
    if not session['uid']:
        flash('게시판을 이용하려면 로그인을 하세요.')
        return redirect('/user/login')

    session['current_user_page'] = page
    offset = (page - 1) * 10
    count = dm.get_user_counts()
    total_page = math.ceil(count / 10)
    start_page = math.floor((page - 1) / 10) * 10 + 1
    end_page = math.ceil(page / 10) * 10
    end_page = total_page if end_page>total_page else end_page
    rows = dm.get_user_list(offset)
    return render_template('user/list.html', menu=menu, user_list=rows,
                            weather=get_weather(),
                            page_no=page, start_page=start_page, 
                            end_page=end_page, total_page=total_page)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html', menu=menu, weather=get_weather())
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        if dm.get_user_info(uid):           # 중복 uid
            flash('중복된 uid 입니다.')
            return redirect(url_for('user_bp.register'))
        elif pwd != pwd2:                   # 패스워드 불일치
            flash('입력한 패스워드가 일치하지 않습니다.')
            return redirect(url_for('user_bp.register'))
        else:
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            dm.insert_user((uid, hashed_pwd, uname, email))
            return redirect('/')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    menu = {'ho':0, 'bb':0, 'us':0, 'li':1, 
            'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
            'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}
    if request.method == 'GET':
        return render_template('user/login.html', menu=menu, weather=get_weather())
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        if not dm.get_user_info(uid):
            flash('잘못된 uid 입니다.')
            return redirect(url_for('user_bp.login'))
        else:
            db_pwd, uname, _, _ = dm.get_user_info(uid)
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            if db_pwd != hashed_pwd:
                flash('잘못된 패스워드입니다.')
                return redirect(url_for('user_bp.login'))
            else:
                flash(f'{uname}님 환영합니다.')
                session['uid'] = uid
                session['uname'] = uname
                return redirect('/')    # 게시판으로 이동

@user_bp.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('uid', None)
        session.pop('uname', None)
        return redirect('/')

@user_bp.route('/update/<uid>', methods=['GET', 'POST'])
def update(uid):
    if request.method == 'GET':
        if session['uid'] == uid:
            row = dm.get_user_info(uid)
            return render_template('user/update.html', menu=menu, weather=get_weather(),
                                    uid=uid, row=row, page=session['current_user_page'])
        else:
            flash('수정 권한이 없습니다.')
            return redirect(url_for('user_bp.list', page=session['current_user_page']))
    else:
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        if pwd:
            if pwd != pwd2:                   # 패스워드 불일치
                flash('입력한 패스워드가 일치하지 않습니다.')
                return redirect(url_for('user_bp.update', uid=uid))
            else:
                pwd_sha256 = hashlib.sha256(pwd.encode())
                hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
        else:
            hashed_pwd = request.form['hashed_pwd']
        dm.update_user((hashed_pwd, uname, email, uid))
        return redirect(url_for('user_bp.list', page=session['current_user_page']))


@user_bp.route('/delete/<uid>', methods=['GET'])
def delete(uid):
    if session['uid'] == 'admin':
        return render_template('user/delete.html', menu=menu, weather=get_weather(),
                                uid=uid, page=session['current_user_page'])
    else:
        flash('권한이 없습니다. 탈퇴하려면 관리자에게 요청하세요.')
        return redirect(url_for('user_bp.list', page=session['current_user_page']))

@user_bp.route('/deleteConfirm/<uid>', methods=['GET'])
def deleteConfirm(uid):
    dm.delete_user(uid)
    return redirect(url_for('user_bp.list', page=session['current_user_page']))
