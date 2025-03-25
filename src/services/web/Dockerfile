FROM python:3.10-slim

WORKDIR /src

COPY src/services/web/requirements.txt .  
COPY src/services/web /src/services/web

RUN pip install --no-cache-dir -r requirements.txt

COPY src/shared /src/shared
COPY src/config /src/config 

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "your_app:app"]