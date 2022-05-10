"""Testing transaction management"""

def test_add_transaction(client, add_user):
    """Test that we can add transaction using the add transaction page"""
    # login to be able to upload a csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a transaction
    response = client.post('/trans/new', data={'amount': -365, 'type': 'DEBIT'})
    # assert that we get redirected to the browse transactions page
    assert '/transactions' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/transactions")
    # assert that we get the expected flash message
    assert b"Transaction added successfully" in response.data
