import json
import mysql.connector as mc

with open('mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

conn = mc.connect(**config)
cur = conn.cursor()

# 사용자 테이블 생성
sql = '''
    CREATE TABLE if NOT exists users (
        uid VARCHAR(20) NOT NULL PRIMARY KEY, 
        pwd CHAR(44) NOT NULL, 
        uname VARCHAR(20) DEFAULT 'Guest', 
        email VARCHAR(40) NOT NULL,
        reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        is_deleted INT DEFAULT 0 
    );
'''
cur.execute(sql)

# 관리자/테스트 유저 등록
users = [('admin', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '관리자', 'admin@ckworld.com'),
         ('test', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '테스트', 'test@ckworld.com'),
         ('james', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '제임스', 'james@ckworld.com'),
         ('maria', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '마리아', 'maria@ckworld.com')]
sql = "INSERT INTO users VALUES(%s, %s, %s, %s, default, 0);"
for params in users:
    cur.execute(sql, params)
conn.commit()

# 게시판 테이블 생성
sql = '''
    CREATE TABLE if NOT EXISTS bbs (
        bid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        uid VARCHAR(20) NOT NULL,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(1000),
        modTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        viewCount INT DEFAULT 0,
        replyCount INT DEFAULT 0,
        isDeleted INT DEFAULT 0,
        FOREIGN KEY(uid) REFERENCES users(uid)
    ) AUTO_INCREMENT=1001;
'''
cur.execute(sql)

# 샘플 게시글
contents = [
    ('james', '[문의]AWS EC2 Flask 설치', 'AWS EC2에 어떻게 Flask를 설치했는지 알려주시면 감사하겠습니다.^^'),
    ('maria', '대단한 웹 사이트네요!!!', '멋진 웹 사이트입니다.')
]
sql = 'INSERT INTO bbs(uid, title, content) VALUES(%s,%s,%s);'
for params in contents:
    cur.execute(sql, params)
conn.commit()

# Reply 테이블 생성
sql = '''
    CREATE TABLE if NOT EXISTS reply (
        rid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        bid INT NOT NULL,
        uid VARCHAR(20) NOT NULL,
        content VARCHAR(100),
        regTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        isMine INT DEFAULT 0,
        FOREIGN KEY(bid) REFERENCES bbs(bid),
        FOREIGN KEY(uid) REFERENCES users(uid)
    );
'''
cur.execute(sql)

# 샘플 reply
replies = [
    (1001, 'maria', '저도 궁금합니다.😆', 0),
    (1002, 'james', '저도 동감입니다.😄', 0),
    (1001, 'james', 'email로 문의해 주시면 친절하게 안내해 드릴게요.😄👍😆', 1)
]
sql = 'INSERT INTO reply(bid,uid,content,isMine) VALUES(%s,%s,%s,%s);'
for params in replies:
    cur.execute(sql, params)
conn.commit()

# Reply에 대하여 bbs 조회수 변경
bbs_reply = [(1,2,1001), (1,1,1002)]
sql = 'update bbs set viewCount=%s, replyCount=%s where bid=%s;'
for params in bbs_reply:
    cur.execute(sql, params)
conn.commit()

cur.close()
conn.close()
