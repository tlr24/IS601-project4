"""Tests the simple_pages module"""

def test_main_menu_link(client):
    """Tests the main menu links"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/"' in response.data

def test_request_index(client):
    """Tests the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Home Page" in response.data
