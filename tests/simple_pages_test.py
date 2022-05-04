"""Tests the simple_pages module"""

def test_main_menu_link(client):
    """Tests the main menu links"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/"' in response.data
    assert b'href="/about"' in response.data

def test_request_index(client):
    """Tests the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Home Page" in response.data

def test_request_about(client):
    """Tests the about page"""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data
