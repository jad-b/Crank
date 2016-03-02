FROM python:3-slim

RUN apt-get update && apt-get install -y \
    gcc

COPY requirements.txt /tmp/
RUN pip install -U \
    -r /tmp/requirements.txt

VOLUME /src
WORKDIR /src
