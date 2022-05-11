from flask import Blueprint, url_for, render_template
from flask_login import login_required
from app.db.models import User
from app.transactions.decorators import admin_required

user_mgmt = Blueprint('user_mgmt', __name__, template_folder='templates')

@user_mgmt.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('user_mgmt.retrieve_user', [('user_id', ':id')])
    return render_template('browse.html', data=data, titles=titles, retrieve_url=retrieve_url, User=User, record_type="Users")

@user_mgmt.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_view.html', user=user)
