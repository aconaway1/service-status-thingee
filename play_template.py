from jinja2 import Environment, FileSystemLoader
import yaml
import requests

# data = {"receivers": [ {'address': '1.1.1.1'}, {'address': '2.2.2.2' } ] }

# environment = Environment(loader=FileSystemLoader("templates/"))
# template = environment.get_template("adsb.j2")

# page = template.render(data)

# print(page)

ADSB_RECEIVERS_FILE = "adsb_receivers.yml"
def load_adsb_receivers():
    with open(ADSB_RECEIVERS_FILE, encoding='utf8') as file:
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

adsb_status = get_adsb_status()
    
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("adsb.j2")
page = template.render(receivers=adsb_status)


print(page)