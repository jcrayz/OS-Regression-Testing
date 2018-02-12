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

import sys

#  ========== Paths ==========
# Absolute path for folder where database and logs will be stored.
if sys.platform == 'linux':
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'AllAmericanRegress')
else:
    print('on windows')
    CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
#  ========== Logging ==========
logger = logging.getLogger(__name__)

# Ensure the installation directory exists
if not os.path.isdir(CONFIG_PATH):
    logging.log(logging.DEBUG, "Created config path")
    os.makedirs(CONFIG_PATH)

# Absolute path for database file.
DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
# Absolute path for log file.
LOG_PATH = os.path.join(CONFIG_PATH, 'logs.log')

# Logs to the temp directory under C
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format=
    '[allamericanregress-service] %(asctime)s %(levelname)-7.7s %(message)s',
)