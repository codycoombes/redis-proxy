FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip

COPY ./requirements.txt /redis-proxy-test/requirements.txt

WORKDIR /redis-proxy-test

RUN pip3 install -r requirements.txt

COPY . /redis-proxy-test

CMD [ "python3", "-u", "./redis-proxy-test.py"]