import sqlite3
from . import config

def execute_tests(self):
    """Execute all tests from DB."""
    # iterate over all tests
    try:
        # logging.info('* * Reached execute_tests * *')
        database_connection = sqlite3.connect(config.DB_PATH)
        cursor = database_connection.cursor()
        for p in cursor.execute("""SELECT * FROM registrant"""):
            # substitute the path into the command
            command = p[2].replace('$1', p[1])
            # execute the command
            # child = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
            # wait for it to finish get an exit code, and get text output
            console_output = child.communicate()[0]
            code = child.returncode
            # only log if there was an error
            if code != 0:
                # logging.debug("Test {} failed.".format(p[3]))
                # database_engine.log_executed_test(p[0], console_output, code)
            logging.info("Test {} exited with code {}".format(p[3], code))
            # TODO: record the execution, any failures, and update current records
    except Exception as e:
        logging.exception(str(e))

def get_cursor():
    CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
    DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
    database_connection = sqlite3.connect(DB_PATH)
    return database_connection.cursor()

def get_registrants():
    cursor = get_cursor()
    return cursor.execute("""SELECT * FROM registrant""")

class ExecutionRecord(db.Model):
    """Record when each Registrant is invoked by allamericanregress
    and record timestamps."""
    id = db.Column(db.Integer, primary_key=True)
    os_version = db.Column(db.String())
    timestamp = db.Column(db.Integer)


def record_execution(os_version):
    """Saves records of when tests are executed, preserving the OS version and time of execution.
    This table exists to reduce duplication of information between the CurrentRecords and FailedRecords tables.
    Returns the execution record ID"""
    cursor = get_cursor()
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

def get_last_os_version():
    """Returns the last recorded OS version as '{major}.{minor}.{build}"""
    with connect() as session:
        exec_rec = session.query(models.ExecutionRecord).order_by(
            models.ExecutionRecord.timestamp)[0]
    if exec_rec == None:
        return ""  # Depending on how we use this function, this return val may change
    return exec_rec.os_version