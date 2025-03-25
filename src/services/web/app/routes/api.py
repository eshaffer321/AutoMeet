from flask import Blueprint
from services.web.app.services.suggestion_service import SuggestionsService

bp = Blueprint('api', __name__)

@bp.route("/categories", methods=["GET"])
def get_categories():
    return SuggestionsService.get_categories()

@bp.route("/subcategories/<category>", methods=["GET"])
def get_subcategories(category):
    return SuggestionsService.get_sub_categories(category)