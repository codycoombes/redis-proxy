FROM alpine:3.14

RUN apk add --no-cache python3 py3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "flask", "run", "--with-threads"]