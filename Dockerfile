FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /mentorci

WORKDIR /mentorci

ADD requirements.txt /mentorci/requirements.txt

RUN pip install -r requirements.txt
