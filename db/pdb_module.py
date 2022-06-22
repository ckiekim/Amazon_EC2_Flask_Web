import json
import mysql.connector as mc

with open('./db/mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

def get_pbbs_list(offset=0):
    conn = mc.connect(**config)
    cur = conn.cursor()
    sql = '''SELECT pid, title, co, authors, term, vc FROM bbs AS b
                WHERE isDeleted=0 ORDER BY pid DESC LIMIT 10 offset %s;'''
    cur.execute(sql, (offset,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for row in rows:
        authors = json.loads(row[3])
        res = {'pid':row[0], 'title':row[1], 'co':row[2], 'na':len(authors), 'term':row[4], 'vc':row[5]}
        results.add(res)
    return results
