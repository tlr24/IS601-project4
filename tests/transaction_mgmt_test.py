"""Testing transaction management"""
from app.db import db
from app.db.models import Transaction

def test_add_transaction(client, add_user):
    """Test that we can add transaction using the add transaction page"""
    # login to be able to upload a csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a transaction
    response = client.post('/trans/new', data={'amount': -365, 'type': 'DEBIT'})

    # check that the transaction was added to the db
    assert db.session.query(Transaction).count() == 1
    transaction = Transaction.query.filter_by(amount='-365').first()
    assert transaction.amount == "-365"
    assert transaction.type == "DEBIT"

    # assert that we get redirected to the browse transactions page
    assert '/transactions' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/transactions")
    # assert that we get the expected flash message
    assert b"Transaction added successfully" in response.data


def test_delete_transaction(client, add_user):
    """Test that we can delete a  on the browse transaction page"""
    # login to be able to see the transaction
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a transaction
    client.post('/trans/new', data={'amount': -365, 'type': 'DEBIT'})
    # delete the transaction
    response = client.post('/trans/1/delete')
    # assert that we get redirected to the browse transactions page
    assert '/transactions' in response.headers['Location']
    assert response.status_code == 302

    # check that it was removed from the db
    assert db.session.query(Transaction).count() == 0

    response = client.get("/transactions")
    # assert that we get the expected flash message
    assert b"Transaction Deleted" in response.data

def test_edit_transaction(client, add_user):
    """Test that we can edit a transaction"""
    # login
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a transaction
    client.post('/trans/new', data={'amount': -365, 'type': 'DEBIT'})
    # edit/update the transaction info
    response = client.post('/trans/1/edit', data={'amount': 50, 'type': 'CREDIT'})

    # assert that we get redirected to the browse page
    assert '/transactions' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/transactions")
    # assert that we get the expected flash message
    assert b"Transaction updated successfully" in response.data

    # check that the transaction was updated in the db
    transaction = Transaction.query.filter_by(amount='50').first()
    assert transaction.amount == "50"
    assert transaction.type == "CREDIT"
