from allamericanregress import config
import sqlite3
import logging
logger = logging.getLogger(__name__)


database_connection = sqlite3.connect(config.DB_PATH)
cursor = database_connection.cursor()
for sql_command in config.DB_TABLES:
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as e:  # table already exists
        logger.log(logging.DEBUG, "Ignoring db error: %s", e)


def register_program(name, path):
    logger.log(logging.DEBUG,
               "Attempting to register program name=%s, path=%s", repr(name), repr(path))
    conn = database_connection
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO programs VALUES (null,?,?) """,
                   (name, path))
    conn.commit()
    logger.log(logging.DEBUG, "Successfully registered name=%s, path=%s", repr(
        name), repr(path))
