import flask
from flask import request, redirect, url_for
from allamericanregress import models, database_engine
from allamericanregress.webapp.app_init import app
from allamericanregress.webapp import forms

# ========== Routes ==========


@app.route("/", methods=['GET', 'POST'])
def index():
    flask.flash('thanks!')
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
        'mockup.html',
        context=dict(registrants=database_engine.all_registrants(), form=form))


@app.route("/logs")
def logs():
    return flask.render_template(
        'log_view.html', context=dict(logs=models.Log.query.all()))
