FROM python:3.10-slim

WORKDIR /app
COPY uploader/requirements.txt .  
COPY uploader /app/uploader

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "/app/uploader/upload.py"]