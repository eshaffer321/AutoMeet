from flask import Flask, request
from flask_wtf import CSRFProtect
from config.config import settings
from services.web.app.utils.jinja_utils import format_duration

def create_app():
    app = Flask(__name__, static_folder='./static', template_folder='./templates')
    app.secret_key = settings.web.secret_key # type: ignore
    
    CSRFProtect(app)

    app.jinja_env.filters['format_duration'] = format_duration


    # Register the main blueprint
    from services.web.app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register the API blueprint with a URL prefix if desired
    from services.web.app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.context_processor
    def inject_request():
        return dict(request=request)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)