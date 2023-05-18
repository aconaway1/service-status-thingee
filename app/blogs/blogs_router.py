import requests
import yaml
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

BLOGS_FILE = "blogs.yml"
HTML_TEMPLATES_DIR = "/code/app/templates/"

def load_blogs_info():
    with open(BLOGS_FILE, encoding='utf8') as file:
        return yaml.safe_load(file)

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

blogs_router = APIRouter()

@blogs_router.get('/')
async def blog_status():
    return {'blogs': get_blogs_status()}

@blogs_router.get('/html')
async def blogs_template():
    blogs_status = get_blogs_status()
    
    environment = Environment(loader=FileSystemLoader(HTML_TEMPLATES_DIR))
    template = environment.get_template("blogs.j2")
    page = template.render(blogs=blogs_status)
        
    return HTMLResponse(status_code=200, content=page)