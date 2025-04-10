FROM python:3.10-slim

WORKDIR /src

COPY src/services/notion_export/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-m", "services.notion_export.notion_export"]