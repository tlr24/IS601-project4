"""Tests the songs functionality"""
import pytest
from app.db.models import db, Transaction, User


@pytest.fixture()
def add_user_to_db():
    user = User('a@gmail.com', '12345678', 0)
    db.session.add(user)
    db.session.commit()

def test_adding_transactions(application, add_user_to_db):
    """Test adding transactions"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare transactions to insert
        user.transactions = [Transaction("100", "CREDIT"), Transaction("200", "DEBIT")]
        db.session.commit()
        assert db.session.query(Transaction).count() == 2
        transaction = Transaction.query.filter_by(amount='100').first()
        assert transaction.amount == "100"

def test_updating_transactions(application, add_user_to_db):
    """Test updating transaction"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare songs to edit
        user.transactions = [Transaction("100", "CREDIT")]
        db.session.commit()
        # changing the amount of the transaction
        transaction = Transaction.query.filter_by(amount='100').first()
        assert transaction is not None
        transaction.amount = "10000000"
        db.session.commit()
        updated_transaction = Transaction.query.filter_by(amount='10000000').first()
        assert updated_transaction.amount == "10000000"

def test_deleting_song(application, add_user_to_db):
    """Test deleting the transaction"""
    user = User.query.filter_by(email="a@gmail.com").first()
    # prepare transaction to insert
    user.transactions = [Transaction("100", "CREDIT")]
    db.session.commit()
    transaction = Transaction.query.filter_by(amount='100').first()
    # delete the transaction
    db.session.delete(transaction)
    #assert db.session.query(Transaction).count() == 0

