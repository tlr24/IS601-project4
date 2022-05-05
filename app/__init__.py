"""A simple flask web app"""
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from app.cli import create_database
from app.db import db, database
from app.db.models import User
from app.simple_pages import simple_pages


def page_not_found(e):
    """Set up 404 page for the app"""
    return render_template("404.html"), 404

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")
    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    bootstrap = Bootstrap5(app)
    app.register_blueprint(simple_pages)
    app.register_blueprint(database)
    # add command function to cli commands
    app.cli.add_command(create_database)
    app.register_error_handler(404, page_not_found)
    db.init_app(app)


    return app