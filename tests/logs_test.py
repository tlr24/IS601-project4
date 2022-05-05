import os
from app.logging_config import log_con


def test_request_log_created():
    # the log files get created when the app is created for testing
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    # get the path of the apps log folder
    logdir = os.path.join(root, '../logs')
    # get the path of the request.log file
    log_file = os.path.join(logdir, 'request.log')
    # check that the file exists
    assert os.path.exists(log_file) == True

def test_csv_log_created():
    # the log files get created when the app is created for testing
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    # get the path of the apps log folder
    logdir = os.path.join(root, '../logs')
    # get the path of the csv.log file
    log_file = os.path.join(logdir, 'csv.log')
    # check that the file exists
    assert os.path.exists(log_file) == True

def test_debug_log_created():
    # the log files get created when the app is created for testing
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    # get the path of the apps log folder
    logdir = os.path.join(root, '../logs')
    # get the path of the debug.log file
    log_file = os.path.join(logdir, 'debug.log')
    # check that the file exists
    assert os.path.exists(log_file) == True
