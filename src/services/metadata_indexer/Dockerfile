FROM python:3.10-slim

WORKDIR /src

COPY src/services/metadata_indexer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-m", "services.metadata_indexer.metadata_indexer"]