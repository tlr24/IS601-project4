"""Test login/registration/logout"""
import pytest
from flask import session
from app.db.models import User
# pylint: disable=line-too-long

@pytest.fixture
def add_user(client):
    """Add a user for testing"""
    client.post("register", data={"email": "a@a.com", "password": "123La!", "confirm": "123La!"})

def test_request_main_menu_links(client):
    """Tests that auth links show up in the main menu"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/register"' in response.data
    assert b'href="/login"' in response.data

def test_auth_pages(client):
    """Tests auth pages"""
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

def test_successful_register(client):
    """Tests successful registration"""
    assert client.get("register").status_code == 200
    response = client.post("register", data={"email": "a@a.com", "password": "123La!", "confirm": "123La!"})
    assert "/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with client.application.app_context():
        assert User.query.filter_by(email="a@a.com").first() is not None

def test_register_bad_email(client):
    """Test registering with a bad email"""
    response = client.post("/register", data={"email": "a", "password": "12345678", "confirm": "12345678"})
    # check for status code to be 200 instead of 302, meaning it didn't redirect (didn't pass frontend validation email criteria)
    assert response.status_code == 200

def test_register_password_confirmation(client):
    """Test password confirmation by registering with mismatching passwords"""
    response = client.post("/register", data={"email": "t@a.com", "password": "12345678", "confirm": "87654321"},
                           follow_redirects=True)
    # check for flash message
    assert b"Passwords must match" in response.data

def test_register_bad_password(client):
    """Test registering with a bad password that does not meet criteria"""
    response = client.post("/register", data={"email": "t@email.com", "password": "1", "confirm": "1"})
    # check for status code to be 200 instead of 302, meaning it didn't redirect (didn't pass frontend validation criteria requiring 6 char password)
    assert response.status_code == 200

def test_already_registered(client, add_user):
    """Tests if user already registered"""
    # attempt to add another user with the same email
    response = client.post("register", data={"email": "a@a.com", "password": "123La!", "confirm": "123La!"})
    assert "/login" == response.headers["Location"]
    assert 302 == response.status_code
    with client:
        response = client.get("/login")
        # check for flash message
        assert b"Already Registered" in response.data

def test_successful_login(client, add_user):
    """Tests successful login"""
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    # test that successful login redirects to the index page
    response = client.post("/login", data={"email": "a@a.com", "password": "123La!"})
    assert response.headers["Location"] == "/"

    with client.application.app_context():
        user_id = User.query.filter_by(email="a@a.com").first().get_id()

    # check that the login request set the user_id in the session
    with client:
        client.get("/")
        assert session["_user_id"] == user_id

def test_login_bad_email(client):
    """Test logging in with invalid email"""
    response = client.post("/login", data={"email": "bademail", "password": "12345678"}, follow_redirects=True)
    # check for flash message
    assert b"Invalid username or password" in response.data

def test_login_bad_password(client, add_user):
    """Test logging in with invalid password"""
    response = client.post("/login", data={"email": "a@a.com", "password": "notthepassword"}, follow_redirects=True)
    # check for flash message
    assert b"Invalid username or password" in response.data
