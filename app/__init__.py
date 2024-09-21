from flask import Flask
from app.routes import scraping

def create_app():
    app = Flask(__name__)

    # Register the scraping routes
    app.register_blueprint(scraping)

    return app
