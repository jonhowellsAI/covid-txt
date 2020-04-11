FROM ubuntu:18.04

LABEL maintainer="Jon Howells <info@jonhowells.ai>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip

# TODO change to work with conda yaml
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /app
WORKDIR /app

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 wsgi