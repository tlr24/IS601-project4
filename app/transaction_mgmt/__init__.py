from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.db import db
from app.db.models import Transaction, transaction_user
from app.transaction_mgmt.forms import add_transaction_form, edit_transaction_form

trans_mgmt = Blueprint('trans_mgmt', __name__,
                       template_folder='templates')


@trans_mgmt.route('/trans/new', methods=['POST', 'GET'])
@login_required
def add_transaction():
    form = add_transaction_form()
    if form.validate_on_submit():
        current_user.transactions.append(Transaction(amount=int(form.amount.data), type=form.type.data, user_id=current_user.id))
        db.session.commit()
        flash('Transaction added successfully', 'success')
        return redirect(url_for('transactions.browse_transactions'), 302)
    return render_template('trans_add.html', form=form)

@trans_mgmt.route('/trans/<int:trans_id>/delete', methods=['POST'])
@login_required
def delete_transaction(trans_id):
    db.session.query(transaction_user).filter_by(user_id=current_user.id, transaction_id=trans_id).delete()
    transaction = Transaction.query.get(trans_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction Deleted', 'success')
    return redirect(url_for('transactions.browse_transactions'), 302)

@trans_mgmt.route('/trans/<int:trans_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_transaction(trans_id):
    transaction = Transaction.query.get(trans_id)
    form = edit_transaction_form(obj=transaction)
    if form.validate_on_submit():
        transaction.amount = int(form.amount.data)
        transaction.type = form.type.data
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction updated successfully', 'success')
        return redirect(url_for('transactions.browse_transactions'))
    return render_template('trans_edit.html', form=form)
