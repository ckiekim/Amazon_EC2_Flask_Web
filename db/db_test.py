import json
import mysql.connector as mc

with open('mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

def get_bbs_list(offset=0):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = '''SELECT b.bid, b.uid, u.uname, b.title, b.content, 
                    DATE_FORMAT(b.modTime, '%%Y-%%m-%%d %%H:%%i:%%s') AS modTime,
                    b.viewCount, b.replyCount
                FROM bbs AS b
                JOIN users AS u
                ON b.uid=u.uid
                WHERE b.isDeleted=0
                ORDER BY b.bid DESC 
                LIMIT 10 offset 0;'''
    cur.execute(sql)    #, (offset,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

rows = get_bbs_list()
for row in rows:
    print(row)
