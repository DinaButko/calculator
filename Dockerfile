FROM python:3.9-slim

WORKDIR /calculator

COPY . /calculator

RUN pip install -r requirements.txt



