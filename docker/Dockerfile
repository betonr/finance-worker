FROM betonoronha/homol:python-deploy-v0.0.1

RUN apk update \
    && apk add --virtual build-dependencies \
        build-base python3-bs4 nano

RUN apk add openssl

COPY . /app

WORKDIR /app

RUN pip3 install -e .['all']