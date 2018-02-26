"""regrOS models."""
from allamericanregress.webapp.app_init import db, app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import time

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


class ExecutionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    os_version = db.Column(db.String())
    timestamp = db.Column(db.Integer)

    def pretty_time(self):
        # prefer the abbreviated timezone, but it's not included in python's
        # time library
        return time.strftime("%Y-%m-%d %I:%M:%S %p %Z", time.localtime(self.timestamp))


class CurrentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registrant_id = db.Column(db.Integer, db.ForeignKey(Registrant.id))
    last_execution_id = db.Column(db.Integer, db.ForeignKey(
        ExecutionRecord.id))
    last_successful_execution_id = db.Column(db.Integer,
                                             db.ForeignKey(ExecutionRecord.id))
    registrant = db.relationship(
        Registrant, backref=db.backref('current_records', lazy='dynamic'))


class FailureRecord(db.Model):
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

admin = Admin(app, name='regrOS Admin', template_mode='bootstrap3')

admin.add_view(ModelView(Log, db.session))
admin.add_view(ModelView(Registrant, db.session))
admin.add_view(ModelView(ExecutionRecord, db.session))
admin.add_view(ModelView(CurrentRecord, db.session))
admin.add_view(ModelView(FailureRecord, db.session))
