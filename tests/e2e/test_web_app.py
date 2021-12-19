import pytest

from flask import session
from werkzeug.urls import url_encode


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This WebApp lets users interact with a collection of books.' in response.data

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'User name is required'),
        ('cj', '', b'User name is too short'),
        ('test', '', b'Password required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('kanye', 'Aa1234567', b'That user name is already taken')
))

def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login(user_name='thor', password='Aa1234567')
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thor'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_all_books(client):
    response = client.get("display_all_books")
    assert response.status_code == 200
    assert b"Superman Archives, Vol. 2" in response.data
    assert b"Next page" in response.data
    assert b"Previous page" in response.data

    response = client.get("display_all_books?cursor=5")
    assert b"Seiyuu-ka! 12" in response.data

def test_browse_release_year(client):
    response = client.get("/browse_by_release_year?by_release_year=1887")
    assert response.status_code == 200
    assert b"Vision of Sir Launfal and Other Poems" in response.data
    assert b"1887" in response.data

def test_browse_publisher(client):
    response = client.get("/browse_by_publisher?by_publisher=Marvel")
    assert response.status_code == 200
    assert b"The Thing: Idol of Millions" in response.data
    assert b"Marvel" in response.data

def test_browse_author(client):
    response = client.get("/browse_by_author?by_author=Maki+Minami")
    assert response.status_code == 200
    assert b"Seiyuu-ka! 12" in response.data
    assert b"Maki Minami" in response.data


def test_books_with_review(client):
    response = client.get('/display_all_books?cursor=0&view_reviews_for=707611')
    assert response.status_code == 200
    assert b'The greatest superman ever' in response.data
    assert b'Batman is more OP than superman' in response.data
    assert b'kinda boring ngl' in response.data
    assert b'I wanna go to the moon' in response.data


