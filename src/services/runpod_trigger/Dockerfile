FROM python:3.10-slim

WORKDIR /src

# Copy shared modules and configuration
COPY src/services/runpod_trigger/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/services/runpod_trigger /src/services/runpod_trigger
COPY src/shared /src/shared
COPY src/config /src/config

# Set environment variables
ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

ENTRYPOINT [ "python", "-u", "/src/services/runpod_trigger/main.py" ]
