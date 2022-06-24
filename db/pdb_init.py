import json
import mysql.connector as mc

with open('mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

conn = mc.connect(**config)
cur = conn.cursor()

# 프로젝트 테이블 생성
sql = '''
    CREATE TABLE if NOT EXISTS pbbs (
        pid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(1000),
        cn VARCHAR(100) NOT NULL,
        co VARCHAR(40) NOT NULL,
        authors VARCHAR(400) NOT NULL,
        term VARCHAR(8),
        files VARCHAR(400),
        vc INT DEFAULT 0,
        ht VARCHAR(200),
        days INT DEFAULT 5,
        isDeleted INT DEFAULT 0
    ) AUTO_INCREMENT=101;
'''
cur.execute(sql)

authors = [
        {'name':'제임스', 'email':'james@ckworld.com'},
        {'name':'마리아', 'email':'maria@ckworld.com'}
    ]
files = ['가나다.pdf', 'abc.mp4']
title = '손그림 색칠 플라스크 구현'
content = '손그림 색칠 플라스크 구현 프로젝트'
term = '2022.06'
vc = 3
cn = '지능형 빅데이터 서비스 개발 과정(9,10회차)'
co = '멀티캠퍼스'
ht = ['#인공지능','#GAN','#파이썬','#플라스크','#웹']

sql = '''
    INSERT INTO pbbs(title,content,cn,co,authors,term,files,vc,ht)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''
params = (title,content,cn,co,json.dumps(authors),term,json.dumps(files),vc,json.dumps(ht))
cur.execute(sql, params)
conn.commit()

cur.close()
conn.close()
