FROM python:3.7

RUN apt-get clean && \
    apt-get update && \
    apt-get install -y \
    mysql-client \
    default-libmysqlclient-dev \
    python3-dev

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./ /app

EXPOSE 8080
