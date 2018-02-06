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


def register_program(name, path, command, author):
    """Registers a program with the the DB."""

    if len(name.strip()) == 0:
        raise ValueError('Name can not be empty!')
    if len(path.strip()) == 0:
        raise ValueError('Path can not be empty!')
    if len(command.strip()) == 0:
        raise ValueError('Command can not be empty!')

    args = (name, path, command, author)
    with connect() as session:
        logger.log(logging.DEBUG, "Attempting to register program %s",
                   repr(args))
        new_registrant = models.Registrant(name=name, path=path, command=command, author=author,
                                           timestamp=time.time())
        session.add(new_registrant)
        logger.log(logging.DEBUG, "Successfully registered %s", repr(args))


def deregister_program(entry_id):
    """Remove a registered program from the DB."""
    raise RuntimeError('Not implemented!')
    with connect() as (conn, cursor):
        logger.log(logging.DEBUG, "Attempting to delete program id=%s",
                   entry_id)

        cursor.execute("""DELETE FROM programs WHERE id=?""", (entry_id,))
        logger.log(logging.DEBUG, "Deleted program models.id=%s", entry_id)


def all_registrants():
    """Return all registrant entries."""
    yield from models.Registrant.query.all()

# This method is on its way to deprecation
def log_executed_test(program_id, test_output, exit_code):
    """Save a test result in the DB."""
    raise RuntimeError('Not implemented!')
    with connect() as (conn, cursor):
        cursor.execute(
            """INSERT INTO logs (program_id, date, output, exit_code) VALUES (?, ?, ?, ?)""",
            (program_id, str(time.time()), str(test_output), exit_code))


def record_execution(os_version):
    """Saves records of when tests are executed, preserving the OS version and time of execution.
    This table exists to reduce duplication of information between the CurrentRecords and FailedRecords tables.
    Returns the execution record ID"""
    with connect() as session:
        logger.log(logging.DEBUG, "Attempting to record execution for version %s", os_version)
        new_execution_record = models.ExecutionRecord(os_version=os_version, timestamp=time.time())
        session.add(new_execution_record)
        logger.log(logging.DEBUG, "Successfully recorded execution of %s", os_version)
    return new_execution_record.id


def update_current_record(registrant_id, execution_id, succeeded):
    """Updates or inserts the current record for the given registrant. References the most recent
       execution record and the last successful one (i.e. can be queried to see if the registrant
       succeeded on its most recent execution)"""
    updated_record = models.CurrentRecord(registrant_id=registrant_id, last_execution_id=execution_id)
    if (succeeded):
        updated_record.last_successful_execution_id = execution_id

    with connect() as session:
        session.merge(updated_record)


def record_failure(registrant_id, execution_id, exit_code, message):
    """Saves records of failed test executions' codes and messages, referencing the program ID and execution ID"""
    with connect() as session:
        failure_record = models.FailureRecord(registrant_id=registrant_id, execution_id=execution_id,
                                         exit_code=exit_code, message=message)
        session.add(failure_record)


def all_test_logs():
    """Return all test logs."""
    raise RuntimeError('Not implemented!')
    return models.Log.query.filter()
    with connect() as (conn, cursor):
        for i in cursor.execute("""SELECT * FROM logs"""):
            yield i

def get_current_results():
    """Return the name, pass/fail value, version of last success, and date of last success"""
    with connect() as session:
        # Join the registrant with their latest execution record
        current_results = session.query(models.Registrant, models.CurrentRecord, models.ExecutionRecord).\
            filter(models.Registrant.id == models.CurrentRecord.registrant_id).\
            filter(models.CurrentRecord.last_execution_id == models.ExecutionRecord.id).all()
        augmented_results = [] # current_results is immutable, but we may need to add to the tuples
        for result in current_results:
            registrant = result[0]
            current_record = result[1]
            last_execution_record = result[2]
            # If the registrant failed recently, find its last successful record
            if current_record.last_execution_id is not current_record.last_successful_execution_id:
                last_successful_record = session.query(models.ExecutionRecord).\
                    filter(models.ExecutionRecord.id == current_record.last_successful_execution_id).first()
            else:
                last_successful_record = last_execution_record

            # Add the successful record to the result tuple
            if last_successful_record is not None:
                result = result + (last_successful_record,)
            print(result)
            augmented_results.append(result)
    return augmented_results

        # registrant id = currentRecord.registrant_id, currentRecord.last_execution_id = executionRecord.id,
        # currentRecord.last_successful_execution_id = executionRecord.id (if different from most recent)

def get_last_os_version():
    """Returns the last recorded OS version as '{major}.{minor}.{build}"""
    with connect() as session:
        exec_rec = session.query(models.ExecutionRecord).order_by(models.ExecutionRecord.timestamp)[0]
    if exec_rec == None:
        return "" # Depending on how we use this function, this return val may change
    return exec_rec.os_version

def migrate_programs():
    """Adds each entry from the Programs table to the Registrants table"""
    with connect() as session:
        for program in models.Program.query.all():
            register_program(program.name, program.path, program.command, None)
            print("{} moved to registrants table".format(program.name))
        rows_deleted = models.Program.query.delete()
        print("{} rows deleted".format(rows_deleted))
