from flask import Blueprint, app, render_template, request
from services.web.app.services import RecordingService
from services.web.app.services.suggestion_service import SuggestionsService
from shared.util.logging import logger 

bp = Blueprint('main', __name__)



recordings_data = [
    {"id": "6d8516cf-6bcc-437a-a1d0-95d876111c13", "s3_key": "audio/2025/03/27/1646_20250327 1046 Recording__merged.json", "recording_ended_at": "2025-03-27T16:46:50.061Z"}
]

####################
# Unprocessed Routes
####################
@bp.route("/unprocessed")
def unprocessed():
    recordings = RecordingService.get_unprocessed()
    return render_template("unprocessed/unprocessed.html", recordings=recordings)

#################
# Metadata routes
#################
@bp.route("/metadata/<id>", methods=["GET"])
def update_metadata(id):
    # Fetch recording based on ID – for now, mock it
    recording = next((rec for rec in recordings_data if rec["id"] == id), None)
    if not recording:
        return "Recording not found", 404

    # Get categories from SuggestionsService
    categories = SuggestionsService.get_categories()

    # Render metadata form
    return render_template(
        "metadata/metadata.html",
        recording=recording,
        categories=categories
    )

@bp.route("/update_metadata/<id>", methods=["POST"])
def index_post():
    try:
        form = request.form
        category = form.get("category", "").strip()
        new_category = form.get("new-category", "").strip()
        sub_category = form.get("sub-category", "").strip()
        new_sub_category = form.get("new-subcategory", "").strip()
        company = form.get("company", "").strip()

        # Replace this with your actual file path logic if needed.
        dummy_file_path = "/tmp/fake_interview.wav"

        RecordingService.create(
            dummy_file_path,
            category=category,
            new_category=new_category,
            subcategory=sub_category,
            new_subcategory=new_sub_category,
            company=company
        )

        return render_template('success.html', new_path=dummy_file_path)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return "Error", 500