from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import yaml
from jinja2 import Environment, FileSystemLoader
import requests

ADSB_TEMPLATE = "templates/adsb.j2"
ADSB_RECEIVERS_FILE = "adsb_receivers.yml"
HTML_TEMPLATES_DIR = "/code/app/templates/"

INTERESTING_HEX_FILE = "interesting_calls.yml"

def load_adsb_receivers():
    with open(ADSB_RECEIVERS_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)
    
def load_interesting_hex():
    with open(INTERESTING_HEX_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)
    

def get_adsb_status(receivers: list = load_adsb_receivers()) -> list:
    status_list = []
    for receiver in receivers:
        try:
            r = requests.get(url=f"http://{receiver['address']}/tar1090/data/status.json", timeout=(2, 5))
            status_code = r.status_code
            json_data = r.json()
        except requests.ConnectTimeout as e:
            status_code = 500
            json_data = {'reason': f'Timeout to {receiver}'}
        except requests.ConnectionError as e:
            status_code = 500
            json_data = {'reason': f"Something happened on the way to {receiver['name']}"}
        status_list.append({
                'address': receiver['name'],
                'status': status_code,
                'data': json_data
            })
    return status_list


adsb_router = APIRouter()

@adsb_router.get('/')
async def adsb_status():
    return {'receivers': get_adsb_status()}

@adsb_router.get('/html')
async def adsb_template():
    adsb_status = get_adsb_status()
    
    environment = Environment(loader=FileSystemLoader(HTML_TEMPLATES_DIR))
    template = environment.get_template("adsb.j2")
    page = template.render(receivers=adsb_status)
        
    return HTMLResponse(status_code=200, content=page)


@adsb_router.get('/{passed_receiver}')
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
        return {'state': 'Not found'}
    return {'receivers': get_adsb_status(receivers=receivers)}


