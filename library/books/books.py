import datetime

from flask import Blueprint
from werkzeug.urls import url_encode
from flask import request, render_template, redirect, url_for, session
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Length
import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.utilities.services as utilities_services
import library.books.services as services

from library.authentication.authentication import login_required

# Configure Blueprint.
books_blueprint = Blueprint("books_bp", __name__)


@books_blueprint.route("/add_favourite", methods=["GET", "POST"])
@login_required
def add_favourite():

    # Obtain logged in user's username
    user_name = session["user_name"]

    form = FavouriteForm()

    if form.is_submitted():

        # Extract the book_id from the form (book_id represents the "favourited" book)
        book_id = int(form.book_id.data)

        # Use the service layer to add book to user.favourite_books
        services.add_book_to_favourites(book_id, user_name, repo.repo_instance)

        # Retrieve the favourite book in dict form.
        favourite_book = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all books with the same publishers as the reviewed book
        # and display all the reviews, including the new review

        return redirect(url_for("books_bp.browse_by_favourites"))

    if request.method == "GET":
        print("GET Request")
        # Request is a HTTP GET to display the form.
        # Extract the book_id, representing the book to add to favourites, from a query parameter of the GET request.
        book_id = int(request.args.get("book"))

        # Store the article id in the form.
        form.book_id.data = book_id

    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the book id of the book being reviewed from the form.
        book_id = int(form.book_id.data)

    book = services.get_book(book_id, repo.repo_instance)

    return render_template(
        "books/add_to_favourites.html",
        form=form,
        handler_url=url_for("books_bp.add_favourite"),
    )


@books_blueprint.route("/display_all_books", methods=["GET"])
def display_all_books():

    books_per_page = 5

    cursor_index = request.args.get("cursor")

    if cursor_index is None:
        cursor_index = 0
    else:
        cursor_index = int(cursor_index)

    all_books = services.get_all_books(repo.repo_instance)

    book_to_show_reviews = request.args.get("view_reviews_for")

    if book_to_show_reviews is None:
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    (
        first_page_of_books_url,
        next_page_of_books_url,
        previous_page_of_books_url,
        last_page_of_books_url,
    ) = get_book_first_last_pages(cursor_index, all_books, "books_bp.display_all_books")

    list_of_books_to_show = []
    for index in range(cursor_index, books_per_page + cursor_index):
        try:
            book = services.book_to_dict(all_books[index])
            list_of_books_to_show.append(book)
        except IndexError:
            break

    for book in list_of_books_to_show:
        book["view_review_url"] = url_for(
            "books_bp.display_all_books",
            cursor=cursor_index,
            view_reviews_for=book["id"],
        )
        book["add_review_url"] = url_for("books_bp.review_book", book=book["id"])

        # Confirm add to favourites link
        book["add_to_favourites_url"] = url_for(
            "books_bp.add_favourite", book=book["id"]
        )

    return render_template(
        "books/book.html",
        books=list_of_books_to_show,
        page_title="All Books",
        first_book_page_url=first_page_of_books_url,
        last_page_url=last_page_of_books_url,
        next_page_url=next_page_of_books_url,
        prev_page_url=previous_page_of_books_url,
        show_reviews_for_book=book_to_show_reviews,
    )


def get_book_first_last_pages(cursor, list_of_books, url_for_param, books_per_page=5):
    first_page_of_books_url = url_for(url_for_param, cursor=0)
    last_page_of_books_url = url_for(
        url_for_param,
        cursor=len(list_of_books) - len(list_of_books) % books_per_page
        if len(list_of_books) % books_per_page != 0
        else len(list_of_books) - books_per_page,
    )
    next_page_of_books_url = None
    previous_page_of_books_url = None

    lastpage = len(list_of_books) - books_per_page

    if cursor == 0:
        first_page_of_books_url = None

    if cursor - books_per_page >= 0:
        previous_page_of_books_url = url_for(
            url_for_param, cursor=cursor - books_per_page
        )

    if cursor + books_per_page < len(list_of_books):
        next_page_of_books_url = url_for(url_for_param, cursor=books_per_page + cursor)

    if cursor >= lastpage:
        last_page_of_books_url = None

    return (
        first_page_of_books_url,
        next_page_of_books_url,
        previous_page_of_books_url,
        last_page_of_books_url,
    )


def get_first_prev_next_last_urls_publisher_order(
    cursor, list_of_books, url_for_param, publisher_name, books_per_page=3
):
    first_page_of_books_url = url_for(
        url_for_param, cursor=0, by_publisher=publisher_name
    )
    last_page_of_books_url = url_for(
        url_for_param,
        cursor=len(list_of_books) - len(list_of_books) % books_per_page
        if len(list_of_books) % books_per_page != 0
        else len(list_of_books) - books_per_page,
        by_publisher=publisher_name,
    )
    next_page_of_books_url = None
    previous_page_of_books_url = None
    if cursor == 0:
        first_page_of_books_url = None

    if cursor >= len(list_of_books) - books_per_page:
        last_page_of_books_url = None

    if cursor + books_per_page < len(list_of_books):
        next_page_of_books_url = url_for(
            url_for_param, cursor=cursor + books_per_page, by_publisher=publisher_name
        )

    if cursor - books_per_page >= 0:
        previous_page_of_books_url = url_for(
            url_for_param, cursor=cursor - books_per_page, by_publisher=publisher_name
        )

    return (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    )


def get_first_prev_next_last_urls_author_order(
    cursor, list_of_books, url_for_param, author_name, books_per_page=3
):
    first_page_of_books_url = url_for(url_for_param, cursor=0, by_author=author_name)
    last_page_of_books_url = url_for(
        url_for_param,
        cursor=len(list_of_books) - len(list_of_books) % books_per_page
        if len(list_of_books) % books_per_page != 0
        else len(list_of_books) - books_per_page,
        by_author=author_name,
    )
    next_page_of_books_url = None
    previous_page_of_books_url = None
    if cursor == 0:
        first_page_of_books_url = None

    if cursor >= len(list_of_books) - books_per_page:
        last_page_of_books_url = None

    if cursor + books_per_page < len(list_of_books):
        next_page_of_books_url = url_for(
            url_for_param, cursor=cursor + books_per_page, by_author=author_name
        )

    if cursor - books_per_page >= 0:
        previous_page_of_books_url = url_for(
            url_for_param, cursor=cursor - books_per_page, by_author=author_name
        )

    return (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    )


def get_first_prev_next_last_urls_release_year_order(
    cursor, list_of_books, url_for_param, release_year, books_per_page=3
):
    first_page_of_books_url = url_for(
        url_for_param, cursor=0, by_release_year=release_year
    )
    last_page_of_books_url = url_for(
        url_for_param,
        cursor=len(list_of_books) - len(list_of_books) % books_per_page
        if len(list_of_books) % books_per_page != 0
        else len(list_of_books) - books_per_page,
        by_release_year=release_year,
    )
    next_page_of_books_url = None
    previous_page_of_books_url = None
    if cursor == 0:
        first_page_of_books_url = None

    if cursor >= len(list_of_books) - books_per_page:
        last_page_of_books_url = None

    if cursor + books_per_page < len(list_of_books):
        next_page_of_books_url = url_for(
            url_for_param, cursor=cursor + books_per_page, by_release_year=release_year
        )

    if cursor - books_per_page >= 0:
        previous_page_of_books_url = url_for(
            url_for_param, cursor=cursor - books_per_page, by_release_year=release_year
        )

    return (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    )


@books_blueprint.route("/browse_by_favourites", methods=["GET"])
def browse_by_favourites():
    books_per_page = 5

    cursor_index = request.args.get("cursor")

    if cursor_index is None:
        cursor_index = 0
    else:
        cursor_index = int(cursor_index)

    # Obtain logged in user's username
    user_name = session["user_name"]

    favourite_books = services.get_users_favourite_books(user_name, repo.repo_instance)

    book_to_show_reviews = request.args.get("view_reviews_for")

    if book_to_show_reviews is None:
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    (
        first_page_of_books_url,
        next_page_of_books_url,
        previous_page_of_books_url,
        last_page_of_books_url,
    ) = get_book_first_last_pages(
        cursor_index, favourite_books, "books_bp.browse_by_favourites"
    )

    list_of_books_to_show = favourite_books

    for book in list_of_books_to_show:
        book["view_review_url"] = url_for(
            "books_bp.browse_by_favourites",
            cursor=cursor_index,
            view_reviews_for=book["id"],
        )
        book["add_review_url"] = url_for("books_bp.review_book", book=book["id"])

        # Confirm add to favourites link
        book["add_to_favourites_url"] = url_for(
            "books_bp.add_favourite", book=book["id"]
        )

    return render_template(
        "books/book.html",
        books=list_of_books_to_show,
        page_title="All Books",
        first_book_page_url=first_page_of_books_url,
        last_page_url=last_page_of_books_url,
        next_page_url=next_page_of_books_url,
        prev_page_url=previous_page_of_books_url,
        show_reviews_for_book=book_to_show_reviews,
    )


@books_blueprint.route("/browse_by_publisher", methods=["GET"])
def browse_by_publisher():

    publishers = utilities_services.get_all_publishers(repo.repo_instance)

    publisher_name = request.args.get("by_publisher")
    if publisher_name is None:
        return render_template("publisher/publisher.html", publishers=publishers)

    books_per_page = 5
    cursor = request.args.get("cursor")
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    books_by_publisher = utilities_services.get_books_by_publisher_name(
        publisher_name, repo.repo_instance
    )

    book_to_show_reviews = request.args.get("view_reviews_for")
    # print("btsr:", book_to_show_reviews)
    if book_to_show_reviews is None:
        book_to_show_reviews = -1
    else:
        book_to_show_reviews = int(book_to_show_reviews)

    (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    ) = get_first_prev_next_last_urls_publisher_order(
        cursor, books_by_publisher, "books_bp.browse_by_publisher", publisher_name
    )

    list_of_books_to_show = []
    for i in range(cursor, cursor + books_per_page):
        try:
            book = services.book_to_dict(books_by_publisher[i])
            list_of_books_to_show.append(book)
        except IndexError:
            break

    for book in list_of_books_to_show:
        book["view_review_url"] = url_for(
            "books_bp.browse_by_publisher",
            cursor=cursor,
            by_publisher=publisher_name,
            view_reviews_for=book["id"],
        )
        book["add_review_url"] = url_for("books_bp.review_book", book=book["id"])

        # Confirm add to favourites link
        book["add_to_favourites_url"] = url_for(
            "books_bp.add_favourite", book=book["id"]
        )

    return render_template(
        "books/book.html",
        books=list_of_books_to_show,
        first_book_page_url=first_page_of_books_url,
        last_page_url=last_page_of_books_url,
        next_page_url=next_page_of_books_url,
        prev_page_url=previous_page_of_books_url,
        show_reviews_for_book=book_to_show_reviews,
        publisher_name=publisher_name,
    )


@books_blueprint.route("/browse_by_author", methods=["GET"])
def browse_by_author():

    authors = utilities_services.get_all_authors(repo.repo_instance)
    author_name = request.args.get("by_author")
    if author_name is None:
        return render_template("author/author.html", authors=authors)

    # If a author is specified, then retrieve books to display
    books_per_page = 5
    cursor = request.args.get("cursor")
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    books_by_author = utilities_services.get_books_by_author_name(
        author_name, repo.repo_instance
    )

    book_to_show_reviews = request.args.get("view_reviews_for")
    # print("btsr:", book_to_show_reviews)
    if book_to_show_reviews is None:
        book_to_show_reviews = -1
    else:
        book_to_show_reviews = int(book_to_show_reviews)

    (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    ) = get_first_prev_next_last_urls_author_order(
        cursor, books_by_author, "books_bp.browse_by_author", author_name
    )

    list_of_books_to_show = []
    for i in range(cursor, cursor + books_per_page):
        try:
            book = services.book_to_dict(books_by_author[i])
            list_of_books_to_show.append(book)
        except IndexError:
            break

    for book in list_of_books_to_show:
        book["view_review_url"] = url_for(
            "books_bp.browse_by_author",
            cursor=cursor,
            by_author=author_name,
            view_reviews_for=book["id"],
        )
        book["add_review_url"] = url_for("books_bp.review_book", book=book["id"])

        # Confirm add to favourites link
        book["add_to_favourites_url"] = url_for(
            "books_bp.add_favourite", book=book["id"]
        )

    return render_template(
        "books/book.html",
        books=list_of_books_to_show,
        first_book_page_url=first_page_of_books_url,
        last_page_url=last_page_of_books_url,
        next_page_url=next_page_of_books_url,
        prev_page_url=previous_page_of_books_url,
        show_reviews_for_book=book_to_show_reviews,
        author_name=author_name,
    )


@books_blueprint.route("/browse_by_release_year", methods=["GET"])
def browse_by_release_year():

    all_books = utilities_services.get_all_books(repo.repo_instance)
    release_years = []
    for book in all_books:
        if book.release_year not in release_years and book.release_year is not None:
            release_years.append(book.release_year)
    release_years.sort()
    release_years.append("Unknown")

    release_year = request.args.get("by_release_year")
    print("release_year books.py:", release_year)
    if release_year is None:
        return render_template(
            "release_year/release_year.html", release_years=release_years
        )

    books_per_page = 5
    cursor = request.args.get("cursor")
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    books_by_release_year = []
    for book in all_books:
        if book.release_year is None and release_year == "Unknown":
            books_by_release_year.append(book)
        elif book.release_year is not None and release_year != "Unknown":
            if book.release_year == int(release_year):
                books_by_release_year.append(book)

    book_to_show_reviews = request.args.get("view_reviews_for")
    if book_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent book id.
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    (
        first_page_of_books_url,
        previous_page_of_books_url,
        next_page_of_books_url,
        last_page_of_books_url,
    ) = get_first_prev_next_last_urls_author_order(
        cursor, books_by_release_year, "books_bp.browse_by_release_year", release_year
    )

    list_of_books_to_show = []
    for i in range(cursor, cursor + books_per_page):
        try:
            book = services.book_to_dict(books_by_release_year[i])
            list_of_books_to_show.append(book)
        except IndexError:
            break

    for book in list_of_books_to_show:
        book["view_review_url"] = url_for(
            "books_bp.browse_by_release_year",
            cursor=cursor,
            by_release_year=release_year,
            view_reviews_for=book["id"],
        )
        book["add_review_url"] = url_for("books_bp.review_book", book=book["id"])

        # Confirm add to favourites link
        book["add_to_favourites_url"] = url_for(
            "books_bp.add_favourite", book=book["id"]
        )

    return render_template(
        "books/book.html",
        books=list_of_books_to_show,
        first_book_page_url=first_page_of_books_url,
        last_page_url=last_page_of_books_url,
        next_page_url=next_page_of_books_url,
        prev_page_url=previous_page_of_books_url,
        show_reviews_for_book=book_to_show_reviews,
        release_year=release_year,
    )


@books_blueprint.route("/review", methods=["GET", "POST"])
@login_required
def review_book():
    # Obtain the user name of the currently logged in user.
    user_name = session["user_name"]

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with the book_id, when subsequently called with a HTTP POST request, the book_id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # If the review text has passed data validation
        # Extract the book_id from the form (book_id represents the reviewed book)
        book_id = int(form.book_id.data)

        # Use the service layer to store the new comment.
        services.add_review(book_id, form.review.data, user_name, repo.repo_instance)

        # Retrieve the book in dict form.
        book = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all books with the same publishers as the reviewed book
        # and display all the reviews, including the new review
        return redirect(url_for("books_bp.review_book", book=book["id"]))

    if request.method == "GET":
        print("GET Request")
        # Request is a HTTP GET to display the form.
        # Extract the book_id, representing the book to review, from a query parameter of the GET request.
        book_id = int(request.args.get("book"))

        # Store the article id in the form.
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the book id of the book being reviewed from the form.
        book_id = int(form.book_id.data)

    # For a GET or an unsuccessful POST, retrieve the book to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        "books/reviews.html",
        title="Edit book",
        book=book,
        form=form,
        handler_url=url_for("books_bp.review_book"),
        selected_books=utilities.get_selected_books(),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u"Field must not contain profanity"
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField(
        "Review",
        [
            DataRequired(),
            Length(min=4, message="Your review is too short"),
            ProfanityFree(message="Your review must not contain profanity"),
        ],
    )
    book_id = HiddenField("Book id")
    submit = SubmitField("Submit")


class FavouriteForm(FlaskForm):
    book_id = HiddenField("Book id")
    submit = SubmitField("Add to Favourites")
