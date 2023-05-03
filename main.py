import requests
from fastapi import FastAPI
import yaml

ADSB_RECEIVERS_FILE = "adsb_receivers.yml"
BLOGS_FILE = "blogs.yml"

def load_adsb_receivers():
    with open(ADSB_RECEIVERS_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)
    
    
def load_blogs_info():
    with open(BLOGS_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)
    

def get_adsb_status(receivers: list = load_adsb_receivers()) -> list:
    status_list = []
    for receiver in receivers:
        try:
            r = requests.get(url=f"http://{receiver['address']}/tar1090/data/status.json")
            status_code = r.status_code
            json_data = r.json()
        except requests.ConnectTimeout as e:
            status_code = 500
            json_data = {'reason': f'Timeout to {receiver}'}
        status_list.append({
                'address': receiver['name'],
                'status': status_code,
                'data': json_data
            })
    return status_list


def get_blogs_status():
    status_list = []
    for blog in load_blogs_info():
        try:
            r = requests.get(url=blog['url'])
            status_code = r.status_code
        except requests.ConnectTimeout as e:
            status_code = 500
        status_list.append({
            'name': blog['name'],
            'status': status_code
        })
    return status_list
            
        

app = FastAPI()

@app.get('/')
async def main():
    return {'state': 'whatever, man'}


@app.get('/adsb_status')
async def adsb_status():
    return {'receivers': get_adsb_status()}


@app.get('/adsb_status/{passed_receiver}')
async def adsb_status(passed_receiver: str):
    check = False
    all_receivers = load_adsb_receivers()
    receivers = []
    for checked_receivers in all_receivers:
        if checked_receivers['address'] == passed_receiver or checked_receivers['name'] == passed_receiver:
            check = True
            receivers.append(checked_receivers)
            break
    if not check:
        return {'state': 'None'}
    return {'receivers': get_adsb_status(receivers=receivers)}


@app.get('/blogs')
async def blog_status():
    return {'blogs': get_blogs_status()}