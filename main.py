import sqlite3
import json
from fastapi import FastAPI
from datetime import date, datetime

con = sqlite3.connect('wth.db')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
#query db 
def query_db(query, args=(), one=False):
    cur = con.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

def q_db(qy):
    con.row_factory = row_to_dict
    result = con.execute(qy)
    data = json.dumps(result.fetchall(), default = json_serial)
    data = json.loads(data)
    return data



app = FastAPI()

@app.get("/data_tegangan/{item_id}")
async def read_item(item_id):
    q = q_db('select * from ARUS_TEGANGAN')
    return q

@app.get("/data_energi/{item_id}")
async def read_item(item_id):
    q = q_db('select * from ENERGI')
    return q
#print(json.dumps(q_db, default=json_serial))
#print(cursor.fetchall())
#q = query_db('SELECT * FROM ARUS_TEGANGAN desc')
#print(q)
#data = json.dumps(query_db,default = json_serial)
#print(data)
#conn.execute("INSERT INTO ARUS_TEGANGAN (TANGGAL_JAM, SN_METER, TEGANGAN_R, TEGANGAN_S, TEGANGAN_T, ARUS_R, ARUS_S, ARUS_T, POWER_FAKTOR) VALUES ('01/22/2013 12:21:26', 211244764, 0, 100, 0, 0, 0, 0, 1)");
#conn.execute("INSERT INTO ENERGI (TANGGAL_JAM, SN_METER, kWh_WBP_KINI, kWh_WBP_LALU, kWh_LWBP_KINI, kWh_LWBP_LALU, kWh_TOTAL_KINI, kWh_TOTAL_LALU) VALUES ('01/22/2013 12:20:53', 0, 0,0, 0, 0, 0, 0)");