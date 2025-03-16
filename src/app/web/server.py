from flask import Flask, render_template, request
import os
import shutil
import sys
import threading
import webbrowser
import time
from datetime import datetime
from app.service import SuggestionsService, RecordingService

from app.util import logger

app = Flask(__name__, static_folder="static")


BASE_DIR = os.path.expanduser("~/Interviews")
FILE_TO_PROCESS = None  # Store file path globally
RECORDING_TYPES = ["Interview", "Standup", "1:1", "Retrospective", "Meeting", "Other"]


def move_and_rename_file(original_path, category, sub_category, company):
    """Renames and moves the audio file based on metadata input."""
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        sanitized_name = f"{category}_{sub_category}_{company}_{date}.mp3"

        destination_folder = os.path.join(BASE_DIR, company, category)
        os.makedirs(destination_folder, exist_ok=True)

        new_path = os.path.join(destination_folder, sanitized_name)
        shutil.move(original_path, new_path)

        logger.info(f"File moved successfully: {new_path}")
        return new_path
    except Exception as e:
        logger.error(f"Error moving file: {str(e)}", exc_info=True)
        raise


@app.route("/", methods=["POST"])
def index():
    global FILE_TO_PROCESS
    try:
        print(request.form)
        category = request.form["category"].strip()
        new_category = request.form["new-category"].strip()
        sub_category = request.form["sub-category"].strip()
        new_sub_category = request.form['new-subcategory'].strip()
        company = request.form["company"].strip()

        RecordingService.create(FILE_TO_PROCESS, category=category, new_category=new_category, subcategory=sub_category, new_subcategory=new_sub_category, company=company)


        # new_path = move_and_rename_file(file_path, category=category, sub_category=sub_category, company=company)
        return render_template('success.html', new_path=FILE_TO_PROCESS)
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
    finally:
        delayed_shutdown()


@app.route('/categories', methods=['GET'])
def get_categories():
    return SuggestionsService.get_categories()

@app.route('/subcategories/<category>', methods=['GET'])
def get_subcategories(category):
    return SuggestionsService.get_sub_categories(category)

@app.route("/", methods=["GET"])
def index_get():
    categories = SuggestionsService.get_categories()
    print(categories)
    return render_template("index.html", categories=categories, filename=FILE_TO_PROCESS)


def delayed_shutdown(delay=1):
    """Shut down Flask server after a short delay."""
    logger.info(f"Scheduling delayed shutdown in {delay} second(s)")

    def shutdown():
        try:
            time.sleep(delay)
            logger.info("Shutting down via os exit")
            os._exit(0)
        except Exception as e:
            logger.error(f"Error in shutdown thread: {str(e)}", exc_info=True)

    threading.Thread(target=shutdown).start()


def run_server(file_path, no_popup):
    """Start the Flask server and log the process."""
    global FILE_TO_PROCESS
    FILE_TO_PROCESS = file_path

    if not no_popup:
        url = "http://127.0.0.1:5001/"
        webbrowser.get().open(url)  # Auto-open in browser

    logger.info(f"Starting Flask server for file: {file_path}")
    app.run(debug=False, port=5001, use_reloader=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("No file path provided.")
        sys.exit(1)

    file_path = sys.argv[1]
    no_popup = sys.argv[2] if len(sys.argv) > 2 else None
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        sys.exit(1)

    run_server(file_path, no_popup)