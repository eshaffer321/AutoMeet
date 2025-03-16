from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess
import time

BASE_PATH = "/Users/erickshaffer/code/AutoMeet"
JOURNAL_FILE = os.path.join(BASE_PATH, "data/journal.txt")
PROCESSED_FILE = os.path.join(BASE_PATH, "data/processed.txt")
FAILED_FILE = os.path.join(BASE_PATH, "data/failed.txt")
PROCESS_SCRIPT = os.path.join(BASE_PATH, "scripts/process_audio.sh")

# Ensure required files exist
for file in [JOURNAL_FILE, PROCESSED_FILE, FAILED_FILE]:
    open(file, "a").close()

class JournalHandler(FileSystemEventHandler):
    """Handles updates to the journal file."""
    
    def on_modified(self, event):
        """Triggered when the journal file is modified."""
        if event.src_path == JOURNAL_FILE:
            print("📄 Journal updated! Checking for new tasks...")
            self.process_new_entries()

    def get_unprocessed_files(self):
        """Returns a list of unprocessed files from the journal."""
        with open(JOURNAL_FILE, "r") as journal, open(PROCESSED_FILE, "r") as processed:
            processed_files = set(line.strip() for line in processed)
            return [line.split(",")[0].strip() for line in journal if line.split(",")[0].strip() not in processed_files]

    def process_file(self, file_path):
        """Runs the processing script and logs success/failure."""
        print(f"🚀 Processing: {file_path}")
        try:
            print("Running script!")
            print(f"✅ Completed: {file_path}")
            with open(PROCESSED_FILE, "a") as f:
                f.write(file_path + "\n")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {file_path} (Will retry later)")
            with open(FAILED_FILE, "a") as f:
                f.write(file_path + "\n")

    def process_new_entries(self):
        """Processes all unprocessed files from the journal."""
        unprocessed_files = self.get_unprocessed_files()
        for file_path in unprocessed_files:
            self.process_file(file_path)

def watch():
    """Starts the watcher for journal file changes."""
    observer = Observer()
    event_handler = JournalHandler()
    observer.schedule(event_handler, path=os.path.dirname(JOURNAL_FILE), recursive=False)
    observer.start()
    print("👀 Watcher started, monitoring journal for new entries...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Watcher stopped.")
    observer.join()

if __name__ == "__main__":
    watch()