import flask
from flask import request, redirect, url_for
from allamericanregress import models, database_engine
from .app_init import app

# ========== Routes ==========


@app.route("/")
def index():
    return flask.render_template(
        'mockup.html',
        context=dict(registrants=database_engine.all_registrants()))


@app.route("/logs")
def logs():
    return flask.render_template(
        'log_view.html', context=dict(logs=models.Log.query.all()))


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        database_engine.register_program(request.form["reg_name"],
                                         request.form["reg_filepath"],
                                         request.form["reg_command"])
    return redirect(url_for('home'))
