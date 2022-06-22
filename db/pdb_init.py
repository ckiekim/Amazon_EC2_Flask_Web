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
        desc VARCHAR(1000),
        cn VARCHAR(100),
        co VARCHAR(40),
        authors VARCHAR(200),
        term VARCHAR(8),
        files VARCHAR(100),
        vc INT DEFAULT 0,
        ht VARCHAR(100),
        isDeleted INT DEFAULT 0,
    ) AUTO_INCREMENT=101;
'''
cur.execute(sql)

cur.close()
conn.close()
