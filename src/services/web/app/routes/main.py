import json
from flask import Blueprint, render_template, request
from services.web.app.services import RecordingService, TranscriptionService, SuggestionsService
from shared.util.logging import logger 

bp = Blueprint('main', __name__)

@bp.route("/")
def all_recordings():
    recordings = RecordingService.get_all_recordings()
    return render_template("all_recordings.html", recordings=recordings)

#################
# Metadata routes
#################
@bp.route("/details/edit/<id>", methods=["GET"])
def edit_recording(id):
    recording = RecordingService.get_recording(id)
    subcategories = []
    if recording.subcategory:
        subcategories = SuggestionsService().get_sub_categories(recording.subcategory.name) 

    if not recording:
        return "Recording not found", 404

    transcription = TranscriptionService().get_transcription(recording.s3_key_merged)
    speakers = list(set(entry['speaker'] for entry in transcription['transcription']))

    categories = SuggestionsService.get_categories()
    transcription_formatted = json.dumps(transcription, indent=2)

    return render_template(
        "recording_details_edit.html",
        recording=recording,
        speakers=speakers,
        categories=categories,
        subcategories=subcategories,
        active_tab='edit',
        transcription=transcription_formatted,
    )

@bp.route("/details/overview/<id>", methods=["GET"])
def recording_overview(id):
    recording = RecordingService.get_recording(id)
    if not recording:
        return "Recording not found", 404

    transcription = TranscriptionService().get_transcription(recording.s3_key_merged)
    speakers = list(set(entry['speaker'] for entry in transcription['transcription']))

    transcription_formatted = json.dumps(transcription, indent=2)

    return render_template(
        "recording_details_overview.html",
        recording=recording,
        speakers=speakers,
        active_tab='overview',
        transcription=transcription_formatted,
    )


@bp.route("/update_metadata/<id>", methods=["POST"])
def update_metadata_post(id):
    try:
        recording = RecordingService.get_recording(id)
        if not recording:
            return "Recording not found", 404

        form = request.form
        category_id = form.get("category_id", "").strip()
        category_name = form.get("category_name", "").strip()
        subcategory_id = form.get("sub-category_id", "").strip()
        subcategory_name = form.get("sub-category_name", "").strip()
        company = form.get("company", "").strip()
        updated_transcription = form.get("updated-transcription", "").strip()

        speaker_map = {}
        for key, value in request.form.items():
            if key.startswith("speaker_map[") and key.endswith("]"):
                speaker = key[len("speaker_map["):-1]
                speaker_map[speaker] = value


        TranscriptionService().update_transcription(
            filename=recording.s3_key_merged,
            transcription=updated_transcription,
            speaker_map=speaker_map
        )

        RecordingService.update_recording(
            id,
            category_id=category_id,
            category_name=category_name,
            subcategory_id=subcategory_id,
            subcategory_name=subcategory_name,
            company=company,
            speaker_map=speaker_map
        )

        return render_template('metadata/success.html', new_path=None)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return "Error", 500