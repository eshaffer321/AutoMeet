FROM ghcr.io/jim60105/whisperx:no_model@sha256:186c5474ca758368ac02f98e8101d5a0eb9d70c6d4d0298e0bdde47968a89765

WORKDIR /src

COPY src/services/whisper_worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

ENTRYPOINT ["python", "-m", "services.whisper_worker.whisper_worker"]