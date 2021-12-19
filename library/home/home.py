from flask import Blueprint, render_template

import library.utilities.utilities as utilities


home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home/home.html", books=utilities.get_selected_books(1))
