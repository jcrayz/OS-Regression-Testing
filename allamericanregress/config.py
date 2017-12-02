"""Constants"""
import os
import logging

logger = logging.getLogger(__name__)


CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
DB_TABLES = [
    '''CREATE TABLE logs
                (date text, body text)''',
    '''CREATE TABLE programs
                (id INTEGER PRIMARY KEY, name text, path text)'''

]

LOG_PATH = os.path.join(CONFIG_PATH, 'logs.log')

# ensure the installation directory exists
if not os.path.isdir(CONFIG_PATH):
    print("Create config path")
    os.makedirs(CONFIG_PATH)
if not os.path.isdir(LOG_PATH):
    print("Create config path")
    # os.makedirs(LOG_PATH)


# Logs to the temp directory under C
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[allamericanregress-service] %(asctime)s %(levelname)-7.7s %(message)s',
)
