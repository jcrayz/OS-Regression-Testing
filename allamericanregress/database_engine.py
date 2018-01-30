from allamericanregress import config
import sqlite3
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def connect():
    """Context manager to prevent forgetting to close the DB connection."""
    database_connection = sqlite3.connect(config.DB_PATH)
    cursor = database_connection.cursor()
    yield database_connection, cursor
    database_connection.commit()
    database_connection.close()


# Iterate over configured table names and schemas.
# Create them if they don't yet exist.
# Initialize database connection and cursor
with connect() as (conn, cursor):
    for table_name, sql_command in config.DB_TABLES.items():
        # Command to check if table exists.
        existing_tables = len(list(cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name))))
        if existing_tables == 0:
            cursor.execute(sql_command)
            logger.log(logging.DEBUG, "Created table: %s", sql_command)


def register_program(name, path, command):
    """Insert a program in the the DB."""
    with connect() as (conn, cursor):
        args = (name, path, command)
        logger.log(logging.DEBUG,
                   "Attempting to register program %s", repr(args))
        cursor.execute("""INSERT INTO programs (name,path,command) VALUES (?,?,?) """,
                       args)
        logger.log(logging.DEBUG, "Successfully registered %s", repr(args))


def deregister_program(entry_id):
    """Remove a program entry from the DB."""
    with connect() as (conn, cursor):
        logger.log(logging.DEBUG,
                   "Attempting to delete program id=%s", entry_id)

        cursor.execute("""DELETE FROM programs where id=?""", (entry_id,))
        logger.log(logging.DEBUG,
                   "Deleted program id=%s", entry_id)


def all_entries():
    """Return all program entries."""
    with connect() as (conn, cursor):
        entries = list(cursor.execute("""SELECT * FROM programs"""))
    return entries


def log_executed_test(program_id, test_output, exit_code):
    """Save a test result in the DB."""
    with connect() as (conn, cursor):
        cursor.execute("""INSERT INTO logs (program_id, date, output, exit_code) VALUES (?, ?, ?, ?)""",
                       (program_id, str(time.time()), str(test_output), exit_code))


def all_test_logs():
    """Return all test logs."""
    with connect() as (conn, cursor):
        for i in cursor.execute("""SELECT * FROM logs"""):
            yield i

def get_last_os_version():
    """Return the last recorded OS version"""
    with connect() as(conn, cursor):
        cursor.execute("""SELECT timestamp FROM execution_records ORDER BY timestamp DESC LIMIT 1""")
        return cursor.fetchone()[0]
