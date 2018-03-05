FROM python:3.6-alpine


RUN apk — update upgrade \
  && apk add --update \
  && pip3.6 install --upgrade pip \
  && rm /var/cache/apk/*


ADD . /code

ENV PYTHONPATH /code
WORKDIR /code

RUN pip3 install -U pip && \
  pip3 install -e ".[test]"
