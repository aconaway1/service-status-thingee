import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import yaml
from jinja2 import Environment, FileSystemLoader
from .blogs import blogs_router
from .adsb import adsb_router
import psycopg2

VERSION = 0.2



SYS_STATUS_FILE = "sys_status.yml"



TIMEOUT_TUPLE = (2, 5)


    
def load_sys_status_info():
    with open(SYS_STATUS_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)

app = FastAPI()

app.include_router(blogs_router.blogs_router, prefix="/blogs")
app.include_router(adsb_router.adsb_router, prefix="/adsb")

@app.get('/')
async def main():
    return {'state': 'whatever, man'}


@app.get('/status')
async def status():
    return load_sys_status_info()

@app.get('/db')
async def connect_to_db():
    db_conn = psycopg2.connect(
        host="servicestatusthingee-db-1",
        database="adsb",
        user="adsb_user",
        password="adsb_pass"
    )
    cur = db_conn.cursor()
    cur.execute("select * from adsb_receivers")
    results = cur.fetchall()
    return {
        'results': results
    }
