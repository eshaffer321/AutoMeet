import json
from flask import Blueprint, render_template, request
from services.web.app.services import RecordingService, TranscriptionService, SuggestionsService
from shared.util.logging import logger 

bp = Blueprint('main', __name__)


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
    recording = RecordingService.get_recording(id)
    if not recording:
        return "Recording not found", 404

    transcription = TranscriptionService().get_transcription(recording.s3_key_merged)
    speakers = list(set(entry['speaker'] for entry in transcription))

    categories = SuggestionsService.get_categories()
    transcription_formatted = json.dumps(transcription, indent=2)

    return render_template(
        "metadata/metadata.html",
        recording=recording,
        speakers=speakers,
        categories=categories,
        transcription=transcription_formatted,
    )

@bp.route("/update_metadata/<id>", methods=["POST"])
def update_metadata_post(id):
    try:
        recording = RecordingService.get_recording(id)
        if not recording:
            return "Recording not found", 404

        form = request.form
        category = form.get("category", "").strip()
        new_category = form.get("new-category", "").strip()
        sub_category = form.get("sub-category", "").strip()
        new_sub_category = form.get("new-subcategory", "").strip()
        company = form.get("company", "").strip()
        updated_transcription = form.get("updated_transcription", "").strip()
        speaker_map = request.form.to_dict(flat=False).get('speaker_map', {})

        TranscriptionService().update_transcription(
            filename=recording.s3_key_merged,
            transcription=updated_transcription,
            speaker_map=speaker_map
        )

        RecordingService.update_recording(
            id,
            category=category,
            new_category=new_category,
            subcategory=sub_category,
            new_subcategory=new_sub_category,
            company=company,
            speaker_map=speaker_map
        )

        return render_template('metadata/success.html', new_path=None)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return "Error", 500