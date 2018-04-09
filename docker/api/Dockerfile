FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

MAINTAINER Alberto Montañola <alberto@montanola.eu>

COPY requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -U -r /tmp/requirements.txt

COPY ./src /app


