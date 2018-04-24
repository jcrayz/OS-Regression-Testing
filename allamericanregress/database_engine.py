"""This class provides useful methods for communicating with the SQLite database.
Users can add and remove registrants, add and update execution records, and conveniently
retrieve collections of existing records/registrants.  There is also a method to query
the most recently-tested OS version."""

from allamericanregress import config
import logging
import time
from allamericanregress import models
from contextlib import contextmanager
from allamericanregress.webapp import app_init
from allamericanregress import testing_framework

logger = logging.getLogger(__name__)


@contextmanager
def connect():
    """Context manager to prevent forgetting to close the DB connection.
    Flushes at end."""
    session = app_init.db.session()
    yield session
    session.flush()
    session.commit()


def register_program(name, path, command, author=''):
    """Registers a program with the DB. Name, path, and command are required."""

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
        new_registrant = models.Registrant(
            name=name,
            path=path,
            command=command,
            author=author,
            timestamp=int(time.time()))
        session.add(new_registrant)
        logger.log(logging.DEBUG, "Successfully registered %s", repr(args))

    # On register, the test will execute
    testing_framework.execute_individual_test(new_registrant.id)


def deregister_program(entry_id):
    """Removes the registered program with the given ID from the DB."""
    with connect() as session:
        logger.log(logging.DEBUG, "Attempting to delete program id=%s",
                   entry_id)
        session.query(models.Registrant).filter(
            models.Registrant.id == entry_id).delete()
        session.query(models.FailureRecord).filter(
            models.FailureRecord.registrant_id == entry_id).delete()
        session.query(models.CurrentRecord).filter(
            models.CurrentRecord.registrant_id == entry_id). delete()
        logger.log(logging.DEBUG, "Deleted program id=%s", entry_id)


def all_registrants():
    """Returns all registrant entries."""
    yield from models.Registrant.query.all()


def get_registrant(id_number):
    """Returns the registrant with the given id"""
    return models.Registrant.query.filter(models.Registrant.id == id_number).first()


def get_failure_registrants():
    """Returns all the registrants that have failed on the last run"""
    current_records = models.CurrentRecord.query.all()
    registrants = []
    for record in current_records:
        if record.last_successful_execution_id != record.last_execution_id:
            registrants.append(record.registrant)

    return registrants


def record_execution(os_version):
    """Saves records of when tests are executed, preserving the OS version and time of execution.
    This table exists to reduce duplication of information between the CurrentRecords and FailedRecords tables.
    Returns the execution record ID"""
    with connect() as session:
        logger.log(logging.DEBUG,
                   "Attempting to record execution for version %s", os_version)
        new_execution_record = models.ExecutionRecord(
            os_version=os_version, timestamp=time.time())
        session.add(new_execution_record)
        logger.log(logging.DEBUG, "Successfully recorded execution of %s",
                   os_version)
    return new_execution_record.id


def update_current_record(registrant_id, execution_id, succeeded, execution_time):
    """Updates or inserts the current record for the given registrant. References the most recent
       execution record and the last successful one (i.e. can be queried to see if the registrant
       succeeded on its most recent execution)"""
    with connect() as session:
        # see if there is an existing record for the registrant
        updated_record = session.query(models.CurrentRecord).filter(
            models.CurrentRecord.registrant_id == registrant_id).first()
        if updated_record is None:  # if not, create a new record
            updated_record = models.CurrentRecord(
                registrant_id=registrant_id, last_execution_id=execution_id)
        else:
            updated_record.last_execution_id = execution_id
        if succeeded:
            updated_record.last_successful_execution_id = execution_id

        num_exec = updated_record.num_executions or 0
        total_exec_time = updated_record.total_execution_time or 0
        updated_record.num_executions = num_exec + 1
        updated_record.total_execution_time = total_exec_time + execution_time
        updated_record.last_execution_time = execution_time

        session.merge(updated_record)


def record_failure(registrant_id, execution_id, exit_code, message):
    """Saves records of failed test executions' codes and messages, referencing the program ID and execution ID"""
    with connect() as session:
        failure_record = models.FailureRecord(
            registrant_id=registrant_id,
            execution_id=execution_id,
            exit_code=exit_code,
            message=message)
        session.add(failure_record)


def all_failure_records():
    """Returns all failure records as a list of tuples like (<FailureRecord>, <ExecutionRecord>, <Registrant>)"""
    with connect() as session:
        failure_records = session.query(models.FailureRecord, models.ExecutionRecord, models.Registrant).\
            filter(models.FailureRecord.registrant_id == models.Registrant.id).\
            filter(models.FailureRecord.execution_id ==
                   models.ExecutionRecord.id).all()
    return failure_records


def get_current_results():
    """Returns collection of current results for each registrant in the form of
    <Registrant>, <CurrentRecord>, <LastExecutionRecord>, <LastSuccessfulExecutionRecord>, and <FailureRecord>
    if it exists."""
    with connect() as session:
        # Join the registrant with their latest execution record
        current_results = session.query(models.Registrant, models.CurrentRecord, models.ExecutionRecord).\
            filter(models.Registrant.id == models.CurrentRecord.registrant_id).\
            filter(models.CurrentRecord.last_execution_id ==
                   models.ExecutionRecord.id).all()
        # current_results is immutable, but we may need to add to the tuples
        augmented_results = []
        for result in current_results:
            current_record = result[1]
            last_execution_record = result[2]
            # If the registrant failed recently, find its last successful
            # record and the failure record
            if current_record.last_execution_id is not current_record.last_successful_execution_id:
                last_successful_record = session.query(models.ExecutionRecord).\
                    filter(models.ExecutionRecord.id ==
                           current_record.last_successful_execution_id).first()
                failure_record = get_failure_record(current_record.registrant_id, current_record.last_execution_id)
            else:
                last_successful_record = last_execution_record
                failure_record = None

            # Add the records to the result tuple
            result = result + (last_successful_record, failure_record)
            augmented_results.append(result)
    return augmented_results


def get_failure_record(registrant_id, execution_id):
    """Returns the Failure Record with the associated registrant and execution IDs"""
    with connect() as session:
        record = session.query(models.FailureRecord).filter(models.FailureRecord.registrant_id == registrant_id).\
            filter(models.FailureRecord.execution_id == execution_id).first()
        return record

def get_last_os_version():
    """Returns the last recorded OS version as '{major}.{minor}.{build}"""
    with connect() as session:
        exec_rec = session.query(models.ExecutionRecord).order_by(
            models.ExecutionRecord.timestamp.desc())[0]
    if exec_rec is None:
        return ""  # Depending on how we use this function, this return val may change
    return exec_rec.os_version
