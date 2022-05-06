import os
from click.testing import CliRunner
from app import create_database, create_upload_folder

runner = CliRunner()


def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    dbdir = os.path.join(root, '../database')
    # make a directory if it doesn't exist
    assert os.path.exists(dbdir) == True

def test_create_uploads_folder():
    response = runner.invoke(create_upload_folder)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(root, '../uploads')
    # check if the directory exists
    assert os.path.exists(uploads_dir) == True
