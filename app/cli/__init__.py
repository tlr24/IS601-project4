import os
import click
from flask.cli import with_appcontext
from app.db import db
from app import config


@click.command(name='create-db')
@with_appcontext
def create_database():
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    dbdir = os.path.join(root, '../../database')
    # make a directory if it doesn't exist
    if not os.path.exists(dbdir):
        os.mkdir(dbdir)
    db.create_all()

@click.command(name='create-uploads-folder')
@with_appcontext
def create_upload_folder():
    root = config.Config.BASE_DIR
    # set the name of the apps log folder to logs
    uploadfolder = os.path.join(root,'..',config.Config.UPLOAD_FOLDER)
    # make a directory if it doesn't exist
    if not os.path.exists(uploadfolder):
        os.mkdir(uploadfolder)