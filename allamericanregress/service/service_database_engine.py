import sqlite3
import logging
import time
import os

CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
LOG_PATH = os.path.join(CONFIG_PATH, 'service.log')
LOG_FORMAT = '[regrOS-service] %(levelname)-7.7s %(message)s'
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format=LOG_FORMAT
)

def record_execution(os_version):
    """Saves records of when tests are executed, preserving the OS version and time of execution.
    Returns the execution record ID"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        logging.debug("Attempting to record execution for version %s", os_version)
        cursor.execute("""INSERT INTO execution_record(os_version, timestamp) VALUES ({os_vs}, {time})"""
                       .format(os_vs=os_version, time=time.time()))
        connection.commit()
        row_id = cursor.lastrowid
        connection.close()
        logging.debug("Successfully recorded execution of {}".format(os_version))
        return row_id
    except sqlite3.IntegrityError as e:
        logging.exception(str(e))
        return None

def get_connection():
    """Returns the database connection"""
    # Absolute path for database file.
    DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
    return sqlite3.connect(DB_PATH)


def get_registrants():
    """Returns the list of registrants"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM registrant""")
    registrants = cursor.fetchall()
    connection.close()
    return registrants

def get_current_record(registrant_id):
    """Returns the current record for a given registrant, if it exists"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM current_record WHERE registrant_id={reg_id}"""
                   .format(reg_id=registrant_id))
    current_record = cursor.fetchone()
    connection.close()
    return current_record

def update_current_record(registrant_id, execution_id, succeeded):
    """Updates or inserts the current record for the given registrant. References the most recent
       execution record and the last successful one (i.e. can be queried to see if the registrant
       succeeded on its most recent execution)"""
    try:
        current_record = get_current_record(registrant_id)
        connection = get_connection()
        cursor = connection.cursor()
        if current_record is not None:
            if (succeeded):
                success_exec_id = execution_id
            else:
                success_exec_id = current_record[3]
            # update existing record
            cursor.execute(
                """UPDATE current_record 
                   SET last_execution_id={last_exec}, last_successful_execution_id={last_success}
                   WHERE registrant_id={reg_id}"""
                    .format(last_exec=execution_id, last_success=success_exec_id, reg_id=registrant_id))
        else:
            # insert new record
            if (succeeded):
                cursor.execute(
                    """INSERT INTO current_record(registrant_id, last_execution_id, last_successful_execution_id) 
                       VALUES ({reg_id}, {last_exec}, {last_success})""".format(reg_id=registrant_id,
                                                                                last_exec=execution_id,
                                                                                last_success=execution_id))
            else:
                cursor.execute(
                    """INSERT INTO current_record(registrant_id, last_execution_id)
                       VALUES ({reg_id}, {last_exec})""".format(reg_id=registrant_id,
                                                                last_exec=execution_id))
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as e:
        logging.exception(str(e))

def record_failure(registrant_id, execution_id, exit_code, message):
    """Saves records of failed test executions' codes and messages, referencing the program ID and execution ID"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO failure_record(registrant_id, execution_id, exit_code, message)
                          VALUES ({reg_id}, {exec_id}, {exit_code}, '{msg}')"""
                       .format(reg_id=registrant_id, exec_id=execution_id, exit_code=exit_code, msg=message))
        connection.commit()
        connection.close()
        logging.debug("Recorded failed execution for registrant #{}".format(registrant_id))
    except sqlite3.IntegrityError as e:
        logging.exception(str(e))

def get_last_os_version():
    """Returns the last recorded OS version as '{major}.{minor}.{build}"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT os_version FROM execution_record ORDER BY timestamp LIMIT 1""")
    last_tested_version = cursor.fetchone()
    connection.close()
    if last_tested_version is None:
        return ""  # Depending on how we use this function, this return val may change
    return last_tested_version[0] # fetchone() wraps single value in a tuple