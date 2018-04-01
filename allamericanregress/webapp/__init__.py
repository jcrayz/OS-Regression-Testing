"""This class provides the routes for the Flask web app, handling GET and POST requests."""
import flask
from flask import request, redirect, url_for
from allamericanregress import database_engine, testing_framework
from allamericanregress.webapp.app_init import app
from allamericanregress.webapp import forms
import logging
logger = logging.getLogger(__name__)
logger.debug('index')

# ========== Routes ==========


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    """The index page of the web app displays several tables detailing registrants and their results"""
    # instantiate the form object with request data
    form = forms.RegistrantForm(request.form)
    if request.method == "POST": # handle new registration
        if form.validate():
            database_engine.register_program(
                form.name.data,
                form.path.data,
                form.command.data,
                form.author.data,
            )
            return redirect(url_for('index'))
    return flask.render_template(
        'index.html',
        context=dict(
            current_version=testing_framework.get_current_os_version(),
            registrants=database_engine.all_registrants(),
            test_results=database_engine.get_current_results(),
            form=form))


@app.route("/logs")
def logs():
    """This page displays a table of all failure records"""
    return flask.render_template(
        'failure_log_view.html',
        context=dict(failure_records=database_engine.all_failure_records()))

@app.route("/execute-all")
def execute_all():
    # route for manual execution of tests from app
    testing_framework.execute_tests()
    return redirect(url_for('index'))

@app.route("/execute-failed")
def execute_failed():
    # route for manual execution of failed tests from app
    testing_framework.execute_failed_tests()
    return redirect(url_for('index'))

@app.route("/execute-individual/<int:registrant_id>")
def execute_individual(registrant_id):
    # route for manual execution of individual tests from the app
    testing_framework.execute_individual_test(registrant_id)
    return redirect(url_for('index'))

@app.route("/delete/<int:registrant_id>")
def delete(registrant_id):
    # route for deleting a registrant
    database_engine.deregister_program(registrant_id)
    return redirect(url_for('index'))

def main():
    """File entry point"""
    app.run(debug=True)


if __name__ == '__main__':
    main()