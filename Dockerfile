FROM python:3-slim

COPY *requirements.txt /tmp/
RUN pip install -U \
    -r /tmp/dev_requirements.txt
