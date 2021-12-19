from pathlib import Path
import pytest
from datetime import date, datetime
from library.books import services as b_services
from utils import get_project_root
from library.authentication import services as auth_services
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import RepositoryException

#add_user
def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user

#get_user
def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('kanye')
    assert user == User('kanye', 'imisstheoldkanye432')

#if user None
def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('laqueshalmao')
    assert user is None

#get_number_of_book
def test_repository_can_retrieve_book_count(in_memory_repo):
    book_count = in_memory_repo.get_number_of_book()
    assert book_count == 21

#add_book
def test_repository_add_a_book(in_memory_repo):
    book = Book(1, "Harry Potter and the Chamber of Secrets")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(1) is book

#if book == None
def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    book = in_memory_repo.get_book(101)
    assert book is None

#random_book
def test_repository_get_books_random(in_memory_repo):
    random_books = in_memory_repo.get_books_random(5)
    assert len(random_books) == 5

#all books
def test_repository_get_all_books(in_memory_repo):
    all_books = in_memory_repo.get_all_books()
    assert len(all_books) == 21

#get_book
def test_repository_can_retrieve_a_book(in_memory_repo):
    for book in in_memory_repo.get_all_books():
        assert book == in_memory_repo.get_book(book.book_id)

#get_publisher
def test_repository_can_retrieve_a_publisher(in_memory_repo):
    publishr = in_memory_repo.get_publishers()
    publisher_list = list(set([book.publisher for book in in_memory_repo.get_all_books()]))
    publisher_list.sort()
    for i in range(len(publishr)):
        assert publishr[i] == publisher_list[i]


#add_publisher
def test_repository_add_a_publisher(in_memory_repo):
    publisher_list = list(set([book.publisher for book in in_memory_repo.get_all_books()]))
    publisher_list.sort()
    assert  publisher_list == in_memory_repo.get_publishers()


#get_publisher_name
def test_repository_can_retrieve_publisher_by_name(in_memory_repo):
    publishr = in_memory_repo.get_publisher_by_name("Dargaud")
    assert isinstance(publishr, Publisher)


#if publisher_name None
def test_repository_does_not_retrieve_a_non_existent_publisher_by_name(in_memory_repo):
    publishr = in_memory_repo.get_publisher_by_name('N/A')
    assert publishr is None


#get_book_release_year
def test_repository_can_retrieve_book_release_year(in_memory_repo):
    book_release = in_memory_repo.get_book_release_year(2012)
    assert len(book_release) == 3
    assert isinstance(book_release[0], Book)


#if book_release_year None
def test_repository_does_not_retrieve_a_non_existent_book_release_year(in_memory_repo):
    book_release = in_memory_repo.get_book_release_year(None)
    assert len(book_release) == 4
    #assert book_release is None


#get_book_by_author
def test_repository_can_retrieve_book_by_author(in_memory_repo):
    book_author = in_memory_repo.get_all_authors()
    assert book_author[0].full_name == "Asma"

#if book_by_author None
def test_repository_does_not_retrieve_a_non_existent_book_by_author(in_memory_repo):
    assert in_memory_repo.get_books_by_author(Author(1738, "fake authorrrrr fetty"), ) is None

#get author id
def test_repository_can_retrieve_author_id(in_memory_repo):
    publishr = in_memory_repo.get_author_by_id(6384773)
    assert isinstance(publishr, Author)

    publisher_nonexist = in_memory_repo.get_author_by_id(1)
    assert publisher_nonexist is None


def test_repository_can_retrieve_reviews_for_book(in_memory_repo):
    # review
    reviews_as_dict = b_services.get_review(707611, in_memory_repo)
    assert len(reviews_as_dict) == 4 #cause 4 revs in depo
    book_id = set([review['book_id'] for review in reviews_as_dict])
    assert 707611 in book_id


def test_repository_does_not_retrieve_nonexistent_without_user(in_memory_repo):
    book = in_memory_repo.get_book(707611)
    review = Review("lame ass book", book, 2, None)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_retrieve_nonexistent_without_book(in_memory_repo):
    user = in_memory_repo.get_user("thor")
    review = Review("lame ass book", None, user, datetime)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)




