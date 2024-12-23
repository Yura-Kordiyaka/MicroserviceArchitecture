FROM python:3.12

WORKDIR /auth

RUN apt update && apt -qy upgrade

COPY ./requirements.txt auth/requirements.txt

RUN pip install -r auth/requirements.txt

COPY ./ /auth/

WORKDIR /auth/