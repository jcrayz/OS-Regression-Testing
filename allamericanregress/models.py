"""Database models and admin interface for app."""
from allamericanregress.webapp.app_init import app, db
from allamericanregress import config
import flask_migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import alembic
import logging
import time
logger = logging.getLogger(__name__)

# ========== SQLAlchemy Models ==========


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.String())
    command = db.Column(db.String())

    def __str__(self):
        return self.name


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.Integer, db.ForeignKey(Program.id))
    output = db.Column(db.String())
    exit_code = db.Column(db.Integer)
    date = db.Column(db.Integer)


class Registrant(db.Model):
    """Represent a test suite registered by the user."""
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(), nullable=False)
    command = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    author = db.Column(db.String())
    timestamp = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_age_str(self):
        """Returns the age/registration date of the test in days as a string (e.g. 1 day, today, 3 days)"""
        current_time = time.time()
        age_in_sec = current_time - self.timestamp
        age_in_days = int(round(age_in_sec / (60 * 60 * 24)))
        if (age_in_days > 1):
            return "{} days".format(str(age_in_days))
        elif (age_in_days == 1):
            return "1 day"
        else:
            return "<1 day"


class ExecutionRecord(db.Model):
    """Record when each Registrant is invoked by allamericanregress
    and record timestamps."""
    id = db.Column(db.Integer, primary_key=True)
    os_version = db.Column(db.String())
    timestamp = db.Column(db.Integer)

    def pretty_time(self):
        # prefer the abbreviated timezone, but it's not included in python's
        # time library
        return time.strftime("%Y-%m-%d %I:%M:%S %p %Z",
                             time.localtime(self.timestamp))


class CurrentRecord(db.Model):
    """A summary table of most recent ExecutionRecord for each Registrant."""
    id = db.Column(db.Integer, primary_key=True)
    registrant_id = db.Column(db.Integer, db.ForeignKey(Registrant.id))
    last_execution_id = db.Column(db.Integer, db.ForeignKey(
        ExecutionRecord.id))
    last_successful_execution_id = db.Column(db.Integer,
                                             db.ForeignKey(ExecutionRecord.id))
    num_executions = db.Column(db.Integer)
    # cumulative, for calculating average execution time
    total_execution_time = db.Column(db.Integer)
    last_execution_time = db.Column(db.Integer)

    registrant = db.relationship(
        Registrant, backref=db.backref('current_records', lazy='dynamic'))
    last_execution = db.relationship(
        ExecutionRecord, foreign_keys=[last_execution_id])
    last_successful_execution = db.relationship(
        ExecutionRecord, foreign_keys=[last_successful_execution_id])

    def get_avg_execution_time(self):
        """Returns the average execution time of the test, rounded to hundredths of a second"""
        if (self.num_executions is None):  # necessary check for upgrading rows
            self.num_executions = 0
            self.total_execution_time = 0
        if (self.num_executions < 1):
            return 0
        else:
            return round(self.total_execution_time / self.num_executions, 2)

    def get_last_execution_time(self):
        """Returns the last recorded execution time of the test, rounded to hundredths of a second"""
        if (self.last_execution_time is None):
            return 0
        else:
            return round(self.last_execution_time, 2)


class FailureRecord(db.Model):
    """Record all instances of Registrants' execution failing."""
    id = db.Column(db.Integer, primary_key=True)
    registrant_id = db.Column(
        db.Integer,
        db.ForeignKey(Registrant.id),
    )  # compound key
    registrant = db.relationship(
        Registrant, backref=db.backref('failure_records', lazy='dynamic'))
    execution_id = db.Column(db.Integer, db.ForeignKey(ExecutionRecord.id))
    exit_code = db.Column(db.Integer)
    message = db.Column(db.String())


# ========== Admin Interface ==========
# instantiate admin interface
admin = Admin(app, name='regrOS Admin', template_mode='bootstrap3')
# register model admin views
admin.add_view(ModelView(Log, db.session))
admin.add_view(ModelView(Registrant, db.session, endpoint='model_view_registrant'))
admin.add_view(ModelView(ExecutionRecord, db.session))
admin.add_view(ModelView(CurrentRecord, db.session))
admin.add_view(ModelView(FailureRecord, db.session))


def init():
    # programmatically initialize db with flask_migrate
    with app.app_context():
        try:
            # initialize migrations directory and config files
            flask_migrate.init(config.ALEMBIC_PATH)
        except alembic.util.exc.CommandError as e:
            if 'already exists' in str(e):
                pass
            else:
                logger.debug('flask db init failed: %s', e)
                raise e
        # detect model diffs and generate migration scripts
        flask_migrate.migrate(config.ALEMBIC_PATH)
        try:
            # logger.debug('flask db upgrade')
            # perform the migration
            flask_migrate.upgrade(config.ALEMBIC_PATH)
        except Exception as e:
            logger.debug('flask db upgrade failed: %s', e)
            raise e


init()
