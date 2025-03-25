import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config.config import settings
from shared.redis_client import redis_client
from shared.logging import logger 

DATA_DIR = os.path.expanduser(settings.watcher.data_dir)
JOURNAL_FILE = os.path.join(DATA_DIR, "journal.txt")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed.txt")
FAILED_FILE = os.path.join(DATA_DIR, "failed.txt")

class JournalHandler(FileSystemEventHandler):
    """Handles updates to the journal file."""

    def on_modified(self, event):
        """Triggered when the journal file is modified."""
        if event.src_path == JOURNAL_FILE:
            logger.info("📄 Journal updated! Checking for new tasks...")
            self.process_new_entries()

    def read_processed_files(self):
        """Reads processed files into a set for quick lookup."""
        return self._read_file(PROCESSED_FILE)

    def parse_journal_entry(self, entry: str) -> tuple:
        """Parses a journal entry into a (file_path, timestamp) tuple.
        
        Assumes each entry is of the format 'file_path,timestamp'
        """
        parts = entry.split(",")
        if len(parts) < 2:
            raise ValueError(f"Invalid journal entry: {entry}")
        return parts[0].strip(), parts[1].strip()

    def get_unprocessed_files(self) -> list:
        """Returns a list of tuples containing the file path and timestamp."""
        processed_files = self.read_processed_files()
        journal_entries = self._read_file(JOURNAL_FILE)
        unprocessed_files = []
        
        for entry in journal_entries:
            try:
                file_path, timestamp = self.parse_journal_entry(entry)
                if file_path not in processed_files:
                    unprocessed_files.append((file_path, timestamp))
            except ValueError:
                # Handle the case where the journal entry is invalid, maybe log or skip it
                logger.error(f"Skipping invalid journal entry: {entry}")

        return unprocessed_files

    def process_new_entries(self):
        """Processes all unprocessed files from the journal."""
        for entry in self.get_unprocessed_files():
            self.process_file(entry[0], entry[1])

    def process_file(self, filename: str, timestamp: str):
        """Runs the processing script and logs success/failure."""
        logger.info(f"🚀 Processing: {filename}")
        try:
            self.publish_message(filename, timestamp)
            logger.info(f"✅ Completed: {filename}")
            self._write_file(PROCESSED_FILE, filename)
        except Exception as e:
            logger.error(f"❌ Failed to publish event for: {filename} (Will retry later). Error: {e}")
            self._write_file(FAILED_FILE, filename)

    def publish_message(self, filename, timestamp):
        message = {"file": filename, "timestamp": timestamp}
        redis_client.xadd(settings.redis.streams.journal_steam_name, message)
        logger.info(f"✅ Published event for: {filename}")
        self._write_file(PROCESSED_FILE, filename)
        

    @staticmethod
    def _read_file(file_path):
        """Reads a file and returns its lines as a list."""
        try:
            with open(file_path, "r") as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            return []

    @staticmethod
    def _write_file(file_path, entry):
        """Appends an entry to a file."""
        with open(file_path, "a") as f:
            f.write(entry + "\n")

def ensure_required_files():
    """Ensures required files exist before running the watcher."""
    for file_path in [JOURNAL_FILE, FAILED_FILE, PROCESSED_FILE]:
        if not os.path.exists(file_path):
            open(file_path, "a").close()
            logger.info(f"📄 Created missing file: {file_path}")

import signal

def watch():
    """Starts the watchdog observer without unnecessary polling."""
    ensure_required_files()
    observer = Observer()
    event_handler = JournalHandler()
    observer.schedule(event_handler, path=os.path.dirname(JOURNAL_FILE), recursive=False)
    observer.start()
    
    logger.info("👀 Watcher started, monitoring journal for new entries...")

    def handle_exit(signum, frame):
        """Handles termination signals for a clean exit."""
        logger.info("🛑 Received termination signal. Stopping watcher...")
        observer.stop()

    # Handle SIGINT (Ctrl+C) and SIGTERM (Docker stop)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    observer.join()  # Blocks the main thread without polling

if __name__ == "__main__":
    watch()