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
logger = logging.getLogger(__name__)
FROZEN = getattr(sys, 'frozen', False)
#  ========== Paths ==========
# Absolute path for folder where database and logs will be stored.
if sys.platform == 'linux':
    print('on linux')
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'AllAmericanRegress')
else:
    CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
# Absolute path for database file.
DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
# Absolute path for log file.
LOG_PATH = os.path.join(CONFIG_PATH, 'logs.log')
# Absolute path for the package
if FROZEN:
    logger.debug('Booting up as frozen dist')
    MODULE_PATH = sys._MEIPASS
else:
    logger.critical('Booting up as source dist')
    MODULE_PATH = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
ALEMBIC_PATH = os.path.join(CONFIG_PATH, 'migrations')

# Ensure the installation directory exists
if not os.path.isdir(CONFIG_PATH):
    logging.log(logging.DEBUG, "Created config path")
    os.makedirs(CONFIG_PATH)
