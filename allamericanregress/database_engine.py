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
    cursor = database_connection.cursor()
    cursor.execute("""INSERT INTO programs VALUES (null,?,?) """,
                   (name, path))
    database_connection.commit()
    logger.log(logging.DEBUG, "Successfully registered name=%s, path=%s", repr(
        name), repr(path))


def deregister_program(entry_id):
    logger.log(logging.DEBUG,
               "Attempting to delete program id=%s", entry_id)

    cursor.execute("""DELETE FROM programs where id=?""", (entry_id,))
    database_connection.commit()
    logger.log(logging.DEBUG,
               "Deleted program id=%s", entry_id)
