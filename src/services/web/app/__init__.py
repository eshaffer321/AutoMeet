from flask import Flask, request
from config.config import settings

def create_app():
    # Note: Adjust static_folder and template_folder paths if needed.
    app = Flask(__name__, static_folder='./static', template_folder='./templates')

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
    # This block runs when you execute the package as a module.
    app = create_app()
    app.run(debug=True, port=5001)