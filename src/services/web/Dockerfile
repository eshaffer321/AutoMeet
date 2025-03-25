FROM python:3.10-slim

WORKDIR /src

COPY src/services/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "wsgi:app"]