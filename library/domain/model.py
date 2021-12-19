from datetime import datetime
from typing import List


class Publisher:
    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.name = publisher_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    def __repr__(self):
        return f"<Publisher {self.name}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:
    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    def add_coauthor(self, coauthor):
        if (
            isinstance(coauthor, self.__class__)
            and coauthor.unique_id != self.unique_id
        ):
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f"<Author {self.full_name}, author id = {self.unique_id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)


class Book:
    def __init__(self, book_id: int, book_title: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0 or not isinstance(book_id, int):
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title

        self.__description = None
        self.__publisher = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None

        self.__image_hyperlink: str = None
        self.__hyperlink: str = None
        self.__average_rating = None
        self.__ratings_count = None
        self.__reviews = list()

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @image_hyperlink.setter
    def image_hyperlink(self, hyperlink: str):
        if isinstance(hyperlink, str):
            self.__image_hyperlink = hyperlink.strip()

    @property
    def hyperlink(self) -> str:
        return self.__hyperlink

    @hyperlink.setter
    def hyperlink(self, hyperlink: str):
        if isinstance(hyperlink, str):
            self.__hyperlink = hyperlink.strip()

    def update_average_rating(self, rating: int):
        if isinstance(rating, int):
            if self.__ratings_count is None:
                self.__average_rating = 0.0
                self.__ratings_count = 0
            self.__average_rating = (
                self.ratings_count * self.average_rating + rating
            ) / (self.ratings_count + 1)
            self.__ratings_count += 1
        else:
            raise ValueError("Requires integer value to update average rating")

    def initiliase_rating_and_count(self, avgerage_rating: float, rate: int):
        if isinstance(rate, int) and isinstance(avgerage_rating, float):
            self.__ratings_count = rate
            self.__average_rating = avgerage_rating
        else:
            raise ValueError

    @property
    def average_rating(self):
        return self.__average_rating

    @property
    def ratings_count(self):
        return self.__ratings_count

    @property
    def reviews(self):
        return self.__reviews

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)
        else:
            raise ValueError("Object to add review")

    def __repr__(self):
        return f"<Book {self.title}, book id = {self.book_id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.book_id < other.book_id

    def __hash__(self):
        return hash(self.book_id)


class User:
    def __init__(self, user_name: str, password: str) -> object:
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password

        self.__read_books = []
        self.__reviews = []
        self.__favourites = []  # List of the user's favourite books
        self.__pages_read = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def read_books(self) -> List[Book]:
        return self.__read_books

    @property
    def reviews(self) -> List:
        return self.__reviews

    @property
    def favourites(self) -> List[Book]:
        return self.__favourites

    @property
    def pages_read(self) -> int:
        return self.__pages_read

    def read_a_book(self, book: Book):
        if isinstance(book, Book):
            self.__read_books.append(book)
            if book.num_pages is not None:
                self.__pages_read += book.num_pages

    def add_to_favourites(self, book: Book):
        if isinstance(book, Book):
            if book not in self.__favourites:
                self.__favourites.append(book)

    def add_review(self, review):
        if isinstance(review, Review):
            # Review objects are in practice always considered different due to their timestamp.
            self.__reviews.append(review)

    def __repr__(self):
        return f"<User {self.user_name}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)


class Review:
    def __init__(self, review: str, user: User, book: Book, timestamp: datetime):
        if isinstance(user, User):
            self.__user = user
        else:
            self.__user = None

        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review, str):
            self.__review_text = review.strip()
        else:
            self.__review_text = "N/A"

        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return (
            other.user == self.user
            and other.book == self.book
            and other.review_text == self.review_text
            and other.timestamp == self.timestamp
        )

    def __repr__(self):
        return f"<Review of book {self.book}, user = {self.user}, timestamp = {self.timestamp}>"


def make_review(
    review_text: str, user: User, book: Book, timestamp: datetime = datetime.today()
):
    review = Review(review_text, user, book, timestamp)
    user.add_review(review)
    book.add_review(review)

    return review



class BooksInventory:
    def __init__(self):
        self.__books = {}
        self.__prices = {}
        self.__stock_count = {}

    def add_book(self, book: Book, price: int, nr_books_in_stock: int):
        self.__books[book.book_id] = book
        self.__prices[book.book_id] = price
        self.__stock_count[book.book_id] = nr_books_in_stock

    def remove_book(self, book_id: int):
        self.__books.pop(book_id)
        self.__prices.pop(book_id)
        self.__stock_count.pop(book_id)

    def find_book(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__books[book_id]
        return None

    def find_price(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__prices[book_id]
        return None

    def find_stock_count(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__stock_count[book_id]
        return None

    def search_book_by_title(self, book_title: str):
        for book_id in self.__books.keys():
            if self.__books[book_id].title == book_title:
                return self.__books[book_id]
        return None
