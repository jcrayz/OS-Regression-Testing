"""regrOS models."""
# db = webapp.db
from allamericanregress.webapp.app_init import db, app

# ========== SQLAlchemy Models ==========


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.String())
    command = db.Column(db.String())


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.Integer, db.ForeignKey("program.id"))
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


class ExecutionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    os_version = db.Column(db.String())
    timestamp = db.Column(db.Integer)


class CurrentRecord(db.Model):
    registrant_id = db.Column(
        db.Integer, db.ForeignKey("program.id"), primary_key=True)
    last_execution_id = db.Column(db.Integer,
                                  db.ForeignKey("execution_record.id"))
    last_successful_execution_id = db.Column(
        db.Integer, db.ForeignKey("execution_record.id"))


class FailureRecord(db.Model):
    registrant_id = db.Column(
        db.Integer, db.ForeignKey("program.id"),
        primary_key=True)  # compound key
    execution_id = db.Column(
        db.Integer, db.ForeignKey("execution_record.id"), primary_key=True)
    exit_code = db.Column(db.Integer)
    message = db.Column(db.String())


# ========== Admin Interface ==========
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='regrOS Admin', template_mode='bootstrap3')

admin.add_view(ModelView(Program, db.session))
admin.add_view(ModelView(Log, db.session))
admin.add_view(ModelView(Registrant, db.session))
admin.add_view(ModelView(ExecutionRecord, db.session))
admin.add_view(ModelView(CurrentRecord, db.session))
admin.add_view(ModelView(FailureRecord, db.session))
