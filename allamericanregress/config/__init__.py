"""This module contains constants and configuration values necessary
for the application to run.
This includes:
    Paths of log files and the SQLite DB.
    DB Table definitions.

Directories for these files are automatically created.

The logger is configured.
"""
#  ========== Dependencies ==========
import os
import logging
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
#  ========== Logging ==========
logger = logging.getLogger(__name__)

#  ========== Paths ==========
# Absolute path for folder where database and logs will be stored.
if sys.platform == 'linux':
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'AllAmericanRegress')
else:
    CONFIG_PATH = os.path.join('c:', 'AllAmericanRegress')

# Absolute path for database file.
DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
# Absolute path for log file.
LOG_PATH = os.path.join(CONFIG_PATH, 'logs.log')

#  ========== Flask App ==========
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
# initialize SQLAlchemy engine
db = SQLAlchemy(app)
# initialize migration engine
migrate = Migrate(app, db)


# ========== SQLAlchemy Models ==========


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.String())
    command = db.Column(db.String())


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.Integer, db.ForeignKey("program.id"))
    output = db.Column(db.String())
    exit_code = db.Column(db.Integer)
    date = db.Column(db.Integer)


# ========== Logging ==========
# Ensure the installation directory exists
if not os.path.isdir(CONFIG_PATH):
    logging.log(logging.DEBUG, "Created config path")
    os.makedirs(CONFIG_PATH)


# Logs to the temp directory under C
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[allamericanregress-service] %(asctime)s %(levelname)-7.7s %(message)s',
)
