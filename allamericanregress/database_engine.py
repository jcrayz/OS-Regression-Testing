from allamericanregress import config
from allamericanregress import models
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def connect():
    """Context manager to prevent forgetting to close the DB connection.
    Flushes at end."""
    session = models.db.session()
    yield session
    session.flush()
    session.commit()


def register_program(name, path, command):
    """Insert a program in the the DB."""
    if len(name) == 0:
        raise ValueError('Name can not be empty!')
    if len(path) == 0:
        raise ValueError('Path can not be empty!')
    if len(command) == 0:
        raise ValueError('Command can not be empty!')

    args = (name, path, command)
    with connect() as session:
        logger.log(logging.DEBUG, "Attempting to register program %s",
                   repr(args))
        new_program = models.Program(name=name, path=path, command=command)
        session.add(new_program)
        logger.log(logging.DEBUG, "Successfully registered %s", repr(args))


def deregister_program(entry_id):
    """Remove a program entry from the DB."""
    raise RuntimeError('Not implemented!')
    with connect() as (conn, cursor):
        logger.log(logging.DEBUG, "Attempting to delete program id=%s",
                   entry_id)

        cursor.execute("""DELETE FROM programs where id=?""", (entry_id, ))
        logger.log(logging.DEBUG, "Deleted program models.id=%s", entry_id)


def all_entries():
    """Return all program entries."""
    yield from models.Program.query.all()


def log_executed_test(program_id, test_output, exit_code):
    """Save a test result in the DB."""
    raise RuntimeError('Not implemented!')
    with connect() as (conn, cursor):
        cursor.execute(
            """INSERT INTO logs (program_id, date, output, exit_code) VALUES (?, ?, ?, ?)""",
            (program_id, str(time.time()), str(test_output), exit_code))


def all_test_logs():
    """Return all test logs."""
    raise RuntimeError('Not implemented!')
    return models.Log.query.filter()
    with connect() as (conn, cursor):
        for i in cursor.execute("""SELECT * FROM logs"""):
            yield i


def get_last_os_version():
    """Return the last recorded OS version"""
    raise RuntimeError('Not implemented!')
    with connect() as (conn, cursor):
        cursor.execute(
            """SELECT timestamp FROM execution_records ORDER BY timestamp DESC LIMIT 1"""
        )
        return cursor.fetchone()[0]
