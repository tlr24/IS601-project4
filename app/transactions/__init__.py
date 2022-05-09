import os
import logging
import csv
from flask import Blueprint, current_app, abort, render_template, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
from app import config
from app.db import db
from app.db.models import Transaction
from app.transactions.forms import csv_upload

transaction = Blueprint('transactions', __name__, template_folder='templates')

@transaction.before_app_first_request
def create_upload_folder():
    root = config.Config.BASE_DIR
    uploadfolder = os.path.join(root,'..',config.Config.UPLOAD_FOLDER)
    # make a directory if it doesn't exist
    if not os.path.exists(uploadfolder):
        os.mkdir(uploadfolder)

@transaction.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transaction_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("csv")
        log2 = logging.getLogger("debug")
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        log.info("User " + str(current_user.get_id()) + " uploaded file: " + filename)
        transactions = []
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                log2.debug(row)
                current_user.transactions.append(Transaction(row['AMOUNT'], row['TYPE'], current_user.id))
                db.session.commit()

        return redirect(url_for('transactions.browse_transactions'), 302)
    try:
        return render_template('upload_transactions.html', form=form)
    except TemplateNotFound:
        abort(404)

@transaction.route('/transactions', methods=['GET'], defaults={"page": 1})
@transaction.route('/transactions/<int:page>', methods=['GET'])
@login_required
def browse_transactions(page):
    page = page
    per_page = 1000
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)