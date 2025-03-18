FROM python:3.10-slim

WORKDIR /src

# Copy requirements first (optimizes Docker caching)
COPY src/services/watcher/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Watcher service code
COPY src/services/watcher /src/services/watcher 

# Copy the shared config for production use
COPY src/config /src/config  

# Set Dynaconf environment variable to use the copied config
ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

# Run the watcher
CMD ["python", "-u", "/src/services/watcher/journal_watcher.py"]