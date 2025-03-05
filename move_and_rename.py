from flask import Flask, render_template, request, redirect
import os
import shutil
import sys
import logging
import threading
import webbrowser
from datetime import datetime

from logger import logger

app = Flask(__name__)

BASE_DIR = os.path.expanduser("~/Interviews")
FILE_TO_PROCESS = None  # Store file path globally
RECORDING_TYPES = ["Interview", "Standup", "1:1", "Retrospective", "Meeting", "Other"]

@app.route("/", methods=["GET", "POST"])
def index():
    global FILE_TO_PROCESS
    try:
        if request.method == "POST":
            try:
                logger.info(request.form)
                # Get user input
                recording_type = request.form["recording_type"].strip().lower().replace(" ", "_")
                details = request.form["details"].strip().lower().replace(" ", "_")
                company = request.form["company"].strip().lower().replace(" ", "_") or "internal"

                # Rename and move file
                date = datetime.now().strftime("%Y-%m-%d")
                new_name = f"{recording_type}_{details}_{company}_{date}.mp3"

                destination_folder = os.path.join(BASE_DIR, company, recording_type)
                os.makedirs(destination_folder, exist_ok=True)

                new_path = os.path.join(destination_folder, new_name)
                shutil.move(FILE_TO_PROCESS, new_path)

                logger.info(f"File moved successfully: {new_path}")

                # Close the browser tab & shutdown the Flask server
                shutdown_server()
                return "<script>window.close();</script>Success! File moved to: " + new_path

            except Exception as e:
                logger.error(f"Error processing file: {str(e)}", exc_info=True)
                shutdown_server()
                return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
    return render_template("index.html", recording_types=RECORDING_TYPES)

def shutdown_server():
    """Shutdown Flask server after processing."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        logger.info("Shutting down Flask server.")
        func()
    else:
        logger.warning("Could not find shutdown function for Flask.")

def run_server(file_path):
    """Start the Flask server in a new thread and log the process."""
    global FILE_TO_PROCESS
    FILE_TO_PROCESS = file_path

    logger.info(f"Starting Flask server for file: {file_path}")

    url = "http://127.0.0.1:5001/"
    webbrowser.get().open(url)  # Auto-open in browser

    # Run Flask in a separate thread
    threading.Thread(target=app.run, kwargs={'debug': False, 'port': 5001, 'use_reloader': False}).start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("No file path provided.")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        sys.exit(1)

    run_server(file_path)