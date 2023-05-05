from python:latest
WORKDIR /code
copy requirements.txt /code/requirements.txt
run pip install -r requirements.txt
copy *.yml /code
copy ./app/ /code/app
cmd [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]