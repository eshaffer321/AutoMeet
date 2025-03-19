FROM python:3.10-slim

WORKDIR /src

COPY src/config /src/config 
COPY src/util /src/util

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  