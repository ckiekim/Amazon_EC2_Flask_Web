import json
import mysql.connector as mc

with open('./db/mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

def get_pbbs_list(offset=0):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = '''SELECT pid, title, authors, term, vc, days FROM pbbs
             WHERE isDeleted=0 ORDER BY pid DESC LIMIT 10 offset %s;'''
    cur.execute(sql, (offset,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for row in rows:
        authors = json.loads(row[2])
        res = {'pid':row[0], 'title':row[1], 'na':len(authors), 'term':row[3], 'vc':row[4], 'co':row[5]}
        results.append(res)
    return results

def get_pbbs_data(pid):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = "UPDATE pbbs SET vc=vc+1 WHERE pid=%s;"
    cur.execute(sql, (pid,))
    conn.commit()
    sql = '''SELECT pid, title, content, cn, co, authors, term, files, vc, ht, days
             FROM pbbs WHERE isDeleted=0 and pid=%s'''
    cur.execute(sql, (pid,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    authors = json.loads(row[5])
    files = json.loads(row[7])
    ht = json.loads(row[9])
    res = {'pid':row[0], 'title':row[1], 'content':row[2], 'cn':row[3], 'co':row[4], 'authors':authors, 
           'term':row[6], 'files':files, 'vc':row[8], 'ht':ht, 'days':row[10]}
    return res

def insert_pbbs(params):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = '''INSERT INTO pbbs(title,content,cn,co,authors,term,files,ht,days)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def get_pbbs_counts():
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = 'SELECT count(*) AS count FROM pbbs WHERE isDeleted=0;'
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]

def update_pbbs(params):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = """UPDATE pbbs SET title=%s,content=%s,cn=%s,co=%s,authors=%s,term=%s,files=%s,ht=%s
             WHERE pid=%s"""
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def delete_pbbs(pid):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = "UPDATE pbbs SET isDeleted=1 WHERE pid=%s;"
    cur.execute(sql, (pid,))
    conn.commit()
    cur.close()
    conn.close()
