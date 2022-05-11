"""Testing user management"""
from app.db import db
from app.db.models import User

def test_retrieve_user(client, add_user):
    """Test viewing a user profile"""
    # login to be able to view users
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # assert that we get the user's information on the view page
    response = client.get('users/1')
    assert b"Profile" in response.data
    assert b"User Email: a@a.com" in response.data


def test_add_user(client, add_user):
    """Test that we can add a user"""
    # login
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a user
    response = client.post('/users/new', data={'email': 't@t.com', 'password': '123La!', 'confirm': '123La!'})

    # check that the user was added to the db
    assert db.session.query(User).count() == 2
    user = User.query.filter_by(email='t@t.com').first()
    assert user.email == 't@t.com'

    # assert that we get redirected to the browse page
    assert '/users' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/user")
    # assert that we get the expected flash message
    assert b"New user was added" in response.data


def test_edit_user(client, add_user):
    """Test that we can edit a user"""
    # login to be able to edit
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # edit/update the user info
    response = client.post('/users/1/edit', data={'about': 'hi there', 'is_admin': '1'})

    # assert that we get redirected to the browse page
    assert '/users' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/users")
    # assert that we get the expected flash message
    assert b"User updated successfully" in response.data

    # check that the user was updated in the db
    user = User.query.filter_by(email='a@a.com').first()
    assert user.about == "hi there"
