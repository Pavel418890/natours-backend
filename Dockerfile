FROM python:3.10.2-slim-buster AS builder

ARG INSTALL_DEV=false

COPY requirements.txt requirements.dev.txt /

RUN pip install --no-cache-dir -U pip setuptools wheel && \
    if [${INSTALL_DEV} == true] ; \
    then \
        pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /requirements.dev.txt ; \
    else \ 
        pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /requirements.txt ; \
    fi


FROM python:3.10.2-slim-buster

ENV PYTHONUNBUFFERED 1

# copy from first layer pip wheels dependencies
COPY --from=builder /app/wheels /wheels

# install dependencies
RUN apt update && \
    apt install -y netcat && \
    pip install --no-cache  /wheels/*  

# make sure that static and media folder before mount volume
# owner will be changed at the finish builing image
RUN mkdir -p /home/app/{static,media} && \
    addgroup --system --gid 1000 app &&\
    adduser --system --gid 1000 --uid 1000 app

WORKDIR /home/app

# copy project
COPY src .

# grant privilege
RUN chown -R 1000:1000 . && chmod +x ./commands/*.sh

# change owner
USER app

