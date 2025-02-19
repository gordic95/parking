FROM python:3.12.0-alpine

ENV  PYTHONDONTWRITEBYTECODE  1


RUN mkdir /my_code
WORKDIR /my_code
COPY requirements.txt /my_code/
COPY start.sh /start.sh
RUN pip install -r requirements.txt --progress-bar off
COPY . /my_code/


