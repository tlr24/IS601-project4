"""Create simple_pages module blueprint and routes"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')

@simple_pages.route("/")
def index():
    """Route to index page"""
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)