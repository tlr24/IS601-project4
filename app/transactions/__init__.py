import os
from flask import Blueprint
from app import config

transaction = Blueprint('transactions', __name__, template_folder='templates')

@transaction.before_app_first_request
def create_upload_folder():
    root = config.Config.BASE_DIR
    uploadfolder = os.path.join(root,'..',config.Config.UPLOAD_FOLDER)
    # make a directory if it doesn't exist
    if not os.path.exists(uploadfolder):
        os.mkdir(uploadfolder)
