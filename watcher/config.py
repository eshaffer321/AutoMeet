import os

# Journal file path (from env or default)
JOURNAL_FILE = os.getenv("JOURNAL_FILE", "data/journal.txt")

# Use journal's directory as the base path
JOURNAL_DIR = os.path.dirname(os.path.abspath(JOURNAL_FILE))

# Define other file paths relative to the journal location
PROCESSED_FILE = os.path.join(JOURNAL_DIR, "processed.txt")
FAILED_FILE = os.path.join(JOURNAL_DIR, "failed.txt")
PROCESS_SCRIPT = os.path.join(JOURNAL_DIR, "../scripts/process_audio.sh")  # Adjust if necessary

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis_local")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "file_processing")
REDIS_STREAM = os.getenv("REDIS_STREAM", "journal")