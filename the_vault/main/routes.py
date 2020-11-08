"""Import libraries."""
from flask import render_template, Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Return home template."""
    return render_template("home.html.j2")
