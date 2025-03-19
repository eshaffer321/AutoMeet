FROM python:3.10-slim

WORKDIR /src

COPY src/services/watcher/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/services/watcher /src/services/watcher 

COPY src/shared /src/shared
COPY src/config /src/config

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-u", "/src/services/watcher/journal_watcher.py"]