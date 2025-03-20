FROM python:3.10-slim

WORKDIR /src

COPY src/services/whisper_worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/services/whisper_worker /src/services/whisper_worker

COPY src/shared /src/shared
COPY src/config /src/config

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-u", "/src/services/whisper_worker/handler.py", "--rp_serve_api", "--rp_api_host", "0.0.0.0"]