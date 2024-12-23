FROM python:3.12

WORKDIR /email

RUN apt update && apt -qy upgrade

COPY ./requirements.txt notification/requirements.txt

RUN pip install -r notification/requirements.txt

COPY ./ /notification/

WORKDIR /notification/