from flask import Blueprint, render_template, request
from services.web.app.services import RecordingService
from services.web.app.services.suggestion_service import SuggestionsService
from shared.util.logging import logger 

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET"])
def index_get():
    categories = SuggestionsService.get_categories()
    return render_template("index.html", categories=categories, filename=None)

@bp.route("/", methods=["POST"])
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