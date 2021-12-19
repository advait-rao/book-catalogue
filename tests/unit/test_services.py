from datetime import date

import pytest

from library.authentication.services import AuthenticationException
from library.authentication import services as auth_services
from library.books import services as book_services
from library.utilities import services as utility_services
from library.books.services import InvalidYearException

from library.domain.model import Book, User


def test_can_add_user(in_memory_repo):
    new_user_name = "jay-z"
    new_password = "abcd1A23"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict["user_name"] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict["password"].startswith("pbkdf2:sha256:")


def test_cannot_get_user_with_existing_name(in_memory_repo):
    user_name = "kanye"
    password = "imisstheoldkanye432"

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = "pmccartney"
    new_password = "abcd1A23"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = "pmccartney"
    new_password = "abcd1A23"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, "0987654321", in_memory_repo)


def test_cannot_get_book_with_non_existent_id(in_memory_repo):
    book_id = 23

    with pytest.raises(book_services.NonExistentBookException):
        book_services.get_book(book_id, in_memory_repo)


# get_author_id
def test_can_get_auth_with_existent_id(in_memory_repo):
    all_authors = in_memory_repo.get_all_authors()
    for auth in all_authors:
        assert auth == utility_services.get_author_id(auth.unique_id, in_memory_repo)


# get_all_books
def test_can_get_all_books(in_memory_repo):
    assert (
        utility_services.get_all_books(in_memory_repo) == in_memory_repo.get_all_books()
    )


# get_all_authors
def test_can_get_all_authors(in_memory_repo):
    assert (
        utility_services.get_all_authors(in_memory_repo)
        == in_memory_repo.get_all_authors()
    )


# get_all_publishers
def test_can_get_all_publisherrs(in_memory_repo):
    assert (
        utility_services.get_all_publishers(in_memory_repo)
        == in_memory_repo.get_publishers()
    )


# get_books_publishername
def test_get_books_by_publisher_name(in_memory_repo):
    publisher_book = utility_services.get_books_by_publisher_name(
        "Dargaud", in_memory_repo
    )
    book = in_memory_repo.get_book(30128855)
    assert book in publisher_book


# get_users_favourite_books (returns a list of book dictionaries)
def test_can_get_users_favourite_books(in_memory_repo):
    user_name = "advait"
    users_favourite_books = book_services.get_users_favourite_books(
        user_name, in_memory_repo
    )
    assert users_favourite_books == []

    # Creating a user in order to add book to favourites
    user = in_memory_repo.get_user(user_name)
    book = Book(17, "Lord of the Rings")
    user.add_to_favourites(book)
    users_favourite_books = book_services.get_users_favourite_books(
        user_name, in_memory_repo
    )
    favourite_book = users_favourite_books[0]
    assert int(favourite_book["id"]) == 17


# books_by_author
def test_can_get_books_author(in_memory_repo):
    book_dict_service = book_services.get_books_by_author(
        in_memory_repo.get_all_authors()[0], in_memory_repo
    )
    book_id_list = [
        book.book_id
        for book in in_memory_repo.get_books_by_author(
            in_memory_repo.get_all_authors()[0]
        )
    ]
    for book in book_dict_service:
        assert book["id"] in book_id_list


# get_release year
def test_can_get_books_release_year(in_memory_repo):
    books = book_services.get_books_by_release_year(2012, in_memory_repo)
    assert len(books) == 3
    books = book_services.get_books_by_release_year(None, in_memory_repo)
    assert len(books) == 4

    with pytest.raises(InvalidYearException):
        book_services.get_books_by_release_year(-1, in_memory_repo)


# get_book
def test_can_get_book(in_memory_repo):
    book = in_memory_repo.get_book(17405342)
    book_dict = book_services.get_book(17405342, in_memory_repo)

    assert book_dict["id"] == 17405342
    assert book_dict["release_year"] == book.release_year
    assert book_dict["title"] == "Seiyuu-ka! 12"
    assert (
        book_dict["hyperlink"]
        == "https://www.goodreads.com/book/show/17405342-seiyuu-ka-12"
    )
    assert (
        book_dict["image_hyperlink"]
        == "https://images.gr-assets.com/books/1363766802m/17405342.jpg"
    )
    assert book_dict["publisher"] == book.publisher
    assert book_dict["description"] == book.description
    assert book_dict["authors"] == [author.full_name for author in book.authors]
    assert book_dict["average_rating"] == book.average_rating
