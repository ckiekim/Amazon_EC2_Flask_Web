from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash, make_response
import os, math, json
import db.pdb_module as pm
from my_util.weather import get_weather

pbbs_bp = Blueprint('pbbs_bp', __name__)
menu = {'ho':0, 'bb':1, 'ma':0, 'us':0, 'li':0, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0, 'st':0}

@pbbs_bp.route('/list/<int:page>', methods=['GET'])
def list(page):
    if not session['uid']:
        flash('게시판을 이용하려면 로그인을 하세요.')
        return redirect('/user/login')

    session['current_project_page'] = page
    offset = (page - 1) * 10
    count = pm.get_pbbs_counts()
    total_page = math.ceil(count / 10)
    start_page = math.floor((page - 1) / 10) * 10 + 1
    end_page = math.ceil(page / 10) * 10
    end_page = total_page if end_page>total_page else end_page
    rows = pm.get_pbbs_list(offset)
    return render_template('pbbs/list.html', menu=menu, plist=rows,
                            weather=get_weather(),
                            page_no=page, start_page=start_page, 
                            end_page=end_page, total_page=total_page)

@pbbs_bp.route('/view/<int:pid>', methods=['GET'])
def view(pid):
    row = pm.get_pbbs_data(pid)
    return render_template('pbbs/view.html', menu=menu, weather=get_weather(),
                            row=row, page=session['current_project_page'])

def modify_filename(name):
    return name.replace(' ','_')

@pbbs_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session['uid'] != 'admin':
            flash('등록 권한이 없습니다.')
            return redirect(url_for('pbbs_bp.list', page=session['current_project_page']))
        return render_template('pbbs/register.html', menu=menu, weather=get_weather(),
                                page=session['current_project_page'])
    else:
        title = request.form['title'].strip()
        days = int(request.form['days'].strip())
        content = request.form['content'].strip()
        content = content.replace('\r', '')
        content = content.replace('\n', '<br>')
        ht = request.form['ht'].strip()             # hash tag
        ht_list = [tag.strip() for tag in ht.split(',')]
        term = request.form['term'].strip()

        name1 = request.form['name1'].strip()
        email1 = request.form['email1'].strip()
        name2 = request.form['name2'].strip()
        email2 = request.form['email2'].strip()
        name3 = request.form['name3'].strip()
        email3 = request.form['email3'].strip()
        info = request.form['info'].strip()
        authors = []
        authors.append({'name':name1, 'email':email1 if email1 else 'unknown'})
        if name2:
            authors.append({'name':name2, 'email':email2 if email2 else 'unknown'})
        if name3:
            authors.append({'name':name3, 'email':email3 if email3 else 'unknown'})
        if info:
            info_list = [item.strip() for item in info.split(',')]
            for i in range(math.ceil(len(info_list)/2)):
                authors.append({'name':info_list[2*i], 'email':info_list[2*i+1] if info_list[2*i+1] else 'unknown'})
        #print(authors)

        cn = request.form['cn'].strip()             # course name
        co = request.form['co'].strip()             # course organization
        
        files = []
        upload_path = os.path.join(current_app.root_path, 'static/project_upload')
        f_pdf = request.files['pdf']
        if f_pdf:
            fname = modify_filename(f_pdf.filename)
            f_pdf.save(f'{upload_path}/{fname}')
            files.append(fname)
        f_mp4 = request.files['mp4']
        if f_mp4:
            fname = modify_filename(f_mp4.filename)
            f_mp4.save(f'{upload_path}/{fname}')
            files.append(fname)
        file3 = request.files['file3']
        if file3:
            fname = modify_filename(file3.filename)
            file3.save(f'{upload_path}/{fname}')
            files.append(fname)
        file4 = request.files['file4']
        if file4:
            fname = modify_filename(file4.filename)
            file4.save(f'{upload_path}/{fname}')
            files.append(fname)
        print(files)
        params = (title,content,cn,co,json.dumps(authors),term,json.dumps(files),json.dumps(ht_list),days)
        pm.insert_pbbs(params)
        return redirect(url_for('pbbs_bp.list', page=session['current_project_page']))

@pbbs_bp.route('/update/<int:pid>', methods=['GET', 'POST'])
def update(pid):
    if request.method == 'GET':
        if session['uid'] != 'admin':
            flash('수정 권한이 없습니다.')
            return redirect(url_for('pbbs_bp.view', pid=pid))
        row = pm.get_pbbs_data(pid)
        return render_template('pbbs/update.html', menu=menu, weather=get_weather(),
                                row=row, page=session['current_project_page'])
    else:
        pass

@pbbs_bp.route('/delete/<int:pid>', methods=['GET'])
def delete(pid):
    if session['uid'] != 'admin':
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('pbbs_bp.view', pid=pid))
    return render_template('pbbs/delete.html', menu=menu, weather=get_weather(),
                            pid=pid, page=session['current_project_page'])

@pbbs_bp.route('/deleteConfirm/<int:pid>', methods=['GET'])
def deleteConfirm(pid):
    pm.delete_pbbs(pid)
    return redirect(url_for('pbbs_bp.list', page=session['current_project_page']))
