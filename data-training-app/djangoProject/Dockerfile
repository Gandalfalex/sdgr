FROM python:3.11.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get install -y llvm \
    && apt-get clean

RUN apt-get install dos2unix

COPY requirements.txt ./
RUN dos2unix requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /usr/src/app/
RUN mkdir /usr/src/app/saved_models
RUN chmod +x /usr/src/app/saved_models
RUN dos2unix /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
