"""Testing user management"""

def test_retrieve_user(client, add_user):
    """Test viewing a user profile"""
    # login to be able to view users
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # assert that we get the user's information on the view page
    response = client.get('users/1')
    assert b"Profile" in response.data
    assert b"User Email: a@a.com" in response.data
