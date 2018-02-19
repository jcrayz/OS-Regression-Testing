import flask
from flask import request, redirect, url_for
from allamericanregress import database_engine
from allamericanregress.webapp.app_init import app,db
from allamericanregress.webapp import forms

# initialize the databse file and apply migrations
database_engine.init()
# ========== Routes ==========


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    # instantiate the form object with request data
    form = forms.RegistrantForm(request.form)
    if request.method == "POST":
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
            registrants=database_engine.all_registrants(),
            test_results=database_engine.get_current_results(),
            form=form))


@app.route("/logs")
def logs():
    return flask.render_template(
        'failure_log_view.html',
        context=dict(failure_records=database_engine.all_failure_records()))
