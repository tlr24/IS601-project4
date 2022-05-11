from flask import Blueprint, url_for, render_template, flash, redirect
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.db import db
from app.db.models import User
from app.transactions.decorators import admin_required
from app.user_mgmt.forms import add_user_form, edit_user_form

user_mgmt = Blueprint('user_mgmt', __name__, template_folder='templates')

@user_mgmt.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('user_mgmt.retrieve_user', [('user_id', ':id')])
    add_url = 'user_mgmt.add_user'
    edit_url = ('user_mgmt.edit_user', [('user_id', ':id')])
    return render_template('browse.html', data=data, titles=titles, retrieve_url=retrieve_url, add_url=add_url, edit_url=edit_url, User=User, record_type="Users")

@user_mgmt.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_view.html', user=user)

@user_mgmt.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_user():
    form = add_user_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_admin=int(form.is_admin.data))
            db.session.add(user)
            db.session.commit()
            flash('New user was added', 'success')
            return redirect(url_for('user_mgmt.browse_users'))
        else:
            flash('Already Registered')
            return redirect(url_for('user_mgmt.browse_users'))
    return render_template('user_add.html', form=form)

@user_mgmt.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = edit_user_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        user.is_admin = int(form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user_mgmt.browse_users'))
    return render_template('user_edit.html', form=form)
