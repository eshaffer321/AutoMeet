FROM python:3.10-slim

WORKDIR /src

COPY src/services/uploader/requirements.txt .  
COPY src/services/uploader /src/services/uploader

RUN pip install --no-cache-dir -r requirements.txt

COPY src/shared /src/shared
COPY src/config /src/config 

ENV PYTHONPATH=/src
ENV DYNACONF_SETTINGS=/src/config/settings.yaml  

CMD ["python", "-u", "/src/services/uploader/upload.py"]