from allamericanregress import config
from allamericanregress import models
import logging
import time
from contextlib import contextmanager
import flask_migrate
import os
import sys
import alembic

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
        new_registrant = models.Registrant(
            name=name,
            path=path,
            command=command,
            author=author,
            timestamp=time.time())
        session.add(new_registrant)
        logger.log(logging.DEBUG, "Successfully registered %s", repr(args))


def deregister_program(entry_id):
    """Remove a registered program from the DB."""
    with connect() as session:
        logger.log(logging.DEBUG, "Attempting to delete program id=%s",
                   entry_id)
        session.query(models.Registrant).filter(
            models.Registrant.id == entry_id).delete()
        # Should we delete corresponding entries in FailureRecords and
        # CurrentRecords?
        logger.log(logging.DEBUG, "Deleted program models.id=%s", entry_id)


def all_registrants():
    """Return all registrant entries."""
    yield from models.Registrant.query.all()


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


def update_current_record(registrant_id, execution_id, succeeded):
    """Updates or inserts the current record for the given registrant. References the most recent
       execution record and the last successful one (i.e. can be queried to see if the registrant
       succeeded on its most recent execution)"""
    with connect() as session:
        # see if there is an existing record for the registrant
        updated_record = session.query(models.CurrentRecord).filter(
            models.CurrentRecord.registrant_id == registrant_id).first()
        if (updated_record is None):  # if not, create a new record
            updated_record = models.CurrentRecord(
                registrant_id=registrant_id, last_execution_id=execution_id)
        else:
            updated_record.last_execution_id = execution_id
        if (succeeded):
            updated_record.last_successful_execution_id = execution_id

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
    """Return all failure records as a list of tuples like (<FailureRecord>, <ExecutionRecord>, <Registrant>)"""
    with connect() as session:
        failure_records = session.query(models.FailureRecord, models.ExecutionRecord, models.Registrant).\
            filter(models.FailureRecord.registrant_id == models.Registrant.id).\
            filter(models.FailureRecord.execution_id ==
                   models.ExecutionRecord.id).all()
    return failure_records


def get_current_results():
    """Return the name, pass/fail value, version of last success, and date of last success"""
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
            # record
            if current_record.last_execution_id is not current_record.last_successful_execution_id:
                last_successful_record = session.query(models.ExecutionRecord).\
                    filter(models.ExecutionRecord.id ==
                           current_record.last_successful_execution_id).first()
            else:
                last_successful_record = last_execution_record

            # Add the successful record to the result tuple
            if last_successful_record is not None:
                result = result + (last_successful_record, )
            augmented_results.append(result)
    return augmented_results


def get_last_os_version():
    """Returns the last recorded OS version as '{major}.{minor}.{build}"""
    with connect() as session:
        exec_rec = session.query(models.ExecutionRecord).order_by(
            models.ExecutionRecord.timestamp)[0]
    if exec_rec == None:
        return ""  # Depending on how we use this function, this return val may change
    return exec_rec.os_version
