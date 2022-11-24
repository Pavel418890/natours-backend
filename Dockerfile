FROM python:3.10.2-slim-buster AS builder

ARG INSTALL_DEV

COPY requirements.txt requirements.dev.txt /
RUN echo $INSTALL_DEV
RUN pip install --no-cache-dir -U pip setuptools wheel 
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; \
            then \
              pip wheel \
              -v \
              --no-cache-dir \
              --no-deps \
              --wheel-dir=/natours/wheels \
              -r /requirements.dev.txt ; \
            else  \
              pip wheel \
              -v \
              --no-cache-dir \
              --no-deps   \
              --wheel-dir=/natours/wheels \
              -r /requirements.txt ; \ 
            fi"


FROM python:3.10.2-slim-buster

ENV PYTHONUNBUFFERED 1

ARG DOMAIN
ARG BUILD_DATE
ARG VCS_REF
ENV DOMAIN=$DOMAIN

# copy from first layer pip wheels dependencies
COPY --from=builder /natours/wheels /wheels

# install dependencies
RUN apt update && \
    apt install -y netcat && \
    pip install  -U setuptools pip wheel && \
    pip install  --no-cache-dir --no-deps  /wheels/* && \
    # owner will be changed at the finish builing image 
    addgroup --system --gid 1000 natours &&\ adduser --system --gid 1000 --uid 1000 natours WORKDIR /usr/src/natours/ 
# copy project
COPY src .

# grant privilege
RUN chown -R 1000:1000 . && chmod +x ./commands/*.sh

# change owner
USER natours

LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.title="natours-api" \
      org.opencontainers.image.authors="Pavel Lots <plots418890@gmail.com>" \
      org.opencontainers.image.source="https://github.com/pavel418890/natours-backend" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Pavel Lots"


