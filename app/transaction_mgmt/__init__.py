from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import db
from app.db.models import Transaction
from app.transaction_mgmt.forms import add_transaction_form

trans_mgmt = Blueprint('trans_mgmt', __name__,
                       template_folder='templates')


@trans_mgmt.route('/trans/new', methods=['POST', 'GET'])
@login_required
def add_transaction():
    form = add_transaction_form()
    if form.validate_on_submit():
        transaction = Transaction(amount=int(form.amount.data), type=form.type.data, user_id=current_user.id)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully', 'success')
        return redirect(url_for('transactions.browse_transactions'), 302)
    return render_template('trans_add.html', form=form)
