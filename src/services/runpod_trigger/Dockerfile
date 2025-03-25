FROM python:3.10-slim

WORKDIR /src

COPY src/services/watcher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-m", "services.runpod_trigger.runpod_trigger"]