FROM python:latest
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY *.yml /code
COPY ./app/ /code/app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]