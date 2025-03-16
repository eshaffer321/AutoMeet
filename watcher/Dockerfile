FROM python:3.10-slim

WORKDIR /app
COPY watcher/requirements.txt .  
COPY watcher /app/watcher

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/watcher/journal_watcher.py"]