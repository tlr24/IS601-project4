"""Test login/registration/logout"""
from app.db.models import User
# pylint: disable=line-too-long

def test_request_main_menu_links(client):
    """Tests that auth links show up in the main menu"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """Tests auth pages"""
    response = client.get("/register")
    assert response.status_code == 200

def test_successful_register(client):
    """Tests successful registration"""
    assert client.get("register").status_code == 200
    response = client.post("register", data={"email": "a@a.com", "password": "12345678", "confirm": "12345678"})

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
