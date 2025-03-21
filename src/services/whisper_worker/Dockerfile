FROM ghcr.io/jim60105/whisperx:no_model

WORKDIR /src

# Copy shared modules and configuration
COPY src/services/whisper_worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/services/whisper_worker /src/services/whisper_worker
COPY src/shared /src/shared
COPY src/config /src/config

# Set environment variables
ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

ENTRYPOINT [ "python", "-u", "/src/services/whisper_worker/handler.py" ]
