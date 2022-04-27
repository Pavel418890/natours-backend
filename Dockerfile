FROM python:3.10.2-slim-buster AS builder

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel

COPY requirements.txt ./

RUN \
    pip wheel \
    --no-cache-dir \
    --no-deps \
    --wheel-dir /app/wheels \
    -r requirements.txt


FROM python:3.10.2-slim-buster


ENV HOME=/home/app
ENV APP_HOME=/home/app/src
ENV PYTHONUNBUFFERED 1

# install util for dependencies lifecheck
RUN apt update && apt install -y netcat

# make sure that static and media folder before mount volume
# owner will be changed at the finish builing image
RUN mkdir -p /home/app && \
    mkdir $APP_HOME && \
    mkdir $APP_HOME/static && \
    mkdir $APP_HOME/media && \
    addgroup --system --gid 1000 app &&\
    adduser --system --gid 1000 --uid 1000 app

WORKDIR $APP_HOME

# copy from first layer pip wheels dependencies
COPY --from=builder /app/wheels /wheels

# install dependencies and delete temp/test lib files
RUN pip install --no-cache-dir -U pip wheel setuptools && \
    pip install --no-cache  /wheels/*  && \
    find /usr/local/lib/python3.10/site-packages/ \
      -type d -name test -o -name tests \
      -o -type f -name "*.pyc" -o -name "*.pyo" \
      -exec rm -fr "{}" \;

# copy project
COPY src .

# grant privilege
RUN chown -R 1000:1000 . && chmod +x ./commands/*.sh

# change owner
USER app

