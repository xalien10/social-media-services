FROM python:3.10-alpine

RUN apk add gcc musl-dev libffi-dev

WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code/

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt