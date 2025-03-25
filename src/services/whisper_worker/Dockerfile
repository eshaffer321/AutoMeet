FROM ghcr.io/jim60105/whisperx:no_model

WORKDIR /src

COPY src/services/whisper_worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-m", "services.whisper_worker.whisper_worker"]