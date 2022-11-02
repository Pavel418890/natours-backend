FROM python:3.10.2-slim-buster AS builder

ARG INSTALL_DEV=false

COPY requirements.txt requirements.dev.txt /

RUN pip install --no-cache-dir -U pip setuptools wheel && \
    if [${INSTALL_DEV} == true] ; \
    then \
        pip wheel -v --no-cache-dir --no-deps   --wheel-dir=/app/wheels -r /requirements.dev.txt ; \
    else \ 
        pip wheel -v --no-cache-dir --no-deps   --wheel-dir=/app/wheels -r /requirements.txt ; \
    fi


FROM python:3.10.2-slim-buster

ENV PYTHONUNBUFFERED 1

ARG PROJECT_PATH_ARG
ARG DOMAIN_ARG
ENV PROJECT_PATH=$PROJECT_PATH_ARG
ENV DOMAIN=$DOMAIN_ARG

# copy from first layer pip wheels dependencies
COPY --from=builder /app/wheels /wheels

# install dependencies
RUN apt update && \
    apt install -y netcat && \
    pip install -q --progress-bar=off -U setuptools pip wheel && \
    pip install -q --progress-bar=off --no-cache-dir --no-deps  /wheels/* && \
    # owner will be changed at the finish builing image 
    addgroup --system --gid 1000 app &&\
    adduser --system --gid 1000 --uid 1000 app

WORKDIR ${PROJECT_PATH}

# copy project
COPY src .

# grant privilege
#RUN chown -R 1000:1000 . && chmod +x ./commands/*.sh

# change owner
#USER app

