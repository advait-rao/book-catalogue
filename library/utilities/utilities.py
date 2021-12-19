from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import library.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint("utilities_bp", __name__)


def get_selected_books(quantity=5):
    books = services.get_books_random(quantity, repo.repo_instance)
    return books


def get_all_books():
    return repo.repo_instance.get_all_books()
