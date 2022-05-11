"""Tests the transaction functionality"""
import pytest
import csv
import os
from app.db.models import db, Transaction, User


@pytest.fixture()
def add_user_to_db():
    user = User('a@gmail.com', '123La!', 0)
    db.session.add(user)
    db.session.commit()


@pytest.fixture()
def write_test_csv():
    # write a dummy csv file for testing
    header = ['AMOUNT', 'TYPE']
    data = [
        ['100', "CREDIT"],
        ['-200', "DEBIT"],
        ['300', "CREDIT"],
    ]

    with open('transaction_test.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def test_denied_csv_upload_access(client):
    """Testing denying access to uploading CSV files"""
    response = client.get("/transactions/upload")
    assert "/login?next=%2Ftransactions%2Fupload" == response.headers["Location"]
    with client:
        response = client.get("/login")
        # check for flash message
        assert b"Please log in to access this page." in response.data


def test_allowed_csv_upload_access(client, add_user):
    """Testing allowing access to upload CSV files when logged in"""
    # login to be able to upload csvs
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})
    response = client.get("/transactions/upload")
    # check that we made it to the upload page
    assert response.status_code == 200
    assert b"Upload Transactions" in response.data


def test_adding_transactions(application, add_user_to_db):
    """Test adding transactions"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare transactions to insert
        user.transactions = [Transaction("100", "CREDIT", "1"), Transaction("200", "DEBIT", "1")]
        db.session.commit()
        assert db.session.query(Transaction).count() == 2
        transaction = Transaction.query.filter_by(amount='100').first()
        assert transaction.amount == "100"


def test_updating_transactions(application, add_user_to_db):
    """Test updating transaction"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare transactions to edit
        user.transactions = [Transaction("100", "CREDIT", "1")]
        db.session.commit()
        # changing the amount of the transaction
        transaction = Transaction.query.filter_by(amount='100').first()
        assert transaction is not None
        transaction.amount = "10000000"
        db.session.commit()
        updated_transaction = Transaction.query.filter_by(amount='10000000').first()
        assert updated_transaction.amount == "10000000"


def test_deleting_transaction(application, add_user_to_db):
    """Test deleting the transaction"""
    user = User.query.filter_by(email="a@gmail.com").first()
    # prepare transaction to insert
    user.transactions = [Transaction("100", "CREDIT", "1")]
    db.session.commit()
    transaction = Transaction.query.filter_by(amount='100').first()
    # delete the transaction
    db.session.delete(transaction)
    # assert db.session.query(Transaction).count() == 0


def test_upload_csv(client, add_user, write_test_csv):
    """Test uploading and processing a csv file"""
    # login to be able to upload the csv
    response = client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    file = open("transaction_test.csv", 'rb')
    # upload the csv
    response = client.post('/transactions/upload', data={'file': file})
    assert "/dashboard" in response.headers["Location"]
    assert response.status_code == 302

    root = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(root, '../uploads/transaction_test.csv')
    # check that the file was uploaded
    assert os.path.exists(csv_file) == True

    # test that the csv file was processed and the transactions were inserted into the database
    user = User.query.filter_by(email="a@a.com").first()
    assert len(user.transactions) == 3
    assert db.session.query(Transaction).count() == 3
    assert Transaction.query.filter_by(type="CREDIT").first() is not None
    assert Transaction.query.filter_by(type="DEBIT").first() is not None


def test_get_user_balance(client, add_user, write_test_csv):
    """Test correctly calculating and getting the user's balance on the dashboard"""
    # login to upload the csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})
    # upload the test csv
    file = open("transaction_test.csv", 'rb')
    response = client.post('/transactions/upload', data={'file': file})
    assert "/dashboard" in response.headers["Location"]

    # test if the balance is calculated correctly on the dashboard
    response = client.get('/dashboard')
    assert b"Balance: $200.0" in response.data
