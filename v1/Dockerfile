FROM alpine:3.14

USER root

RUN apk add python3 py3-pip bash

RUN pip install flask

COPY app.py /flask/app.py
COPY start.sh /flask/start.sh

## add aws support
RUN pip3 install boto3
RUN pip3 install --no-cache-dir awscli && mkdir -p /root/.aws/


CMD ['/flask/start.sh']
