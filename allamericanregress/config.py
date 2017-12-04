"""Constants"""
import os
import logging
logger = logging.getLogger(__name__)

# Absolute path for folder where database and logs will be stored.
CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
# Absolute path for database file.
DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
# SQLite table schemas and semantic names.
DB_TABLES = {
    'programs': '''CREATE TABLE programs
                (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    path TEXT,
                    command TEXT
                );''',
    'logs': '''CREATE TABLE logs
                (
                    program_id INTEGER,
                    date TEXT,
                    output TEXT,
                    exit_code INTEGER,
                    FOREIGN KEY(program_id) REFERENCES programs(id)
                );''',
}

# Absolute path for log file.
LOG_PATH = os.path.join(CONFIG_PATH, 'logs.log')

# Ensure the installation directory exists
if not os.path.isdir(CONFIG_PATH):
    loggin.log(logging.DEBUG, "Created config path")
    os.makedirs(CONFIG_PATH)


# Logs to the temp directory under C
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[allamericanregress-service] %(asctime)s %(levelname)-7.7s %(message)s',
)
