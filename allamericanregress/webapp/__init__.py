import flask
from flask import request, redirect, url_for
from allamericanregress import models, database_engine
from .app_init import app, db

# ========== Routes ==========


@app.route("/")
@app.route("/index")
def index():
    return flask.render_template(
        'index.html',
        context=dict(
            registrants=database_engine.all_registrants(),
            test_results=database_engine.get_current_results()))


@app.route("/logs")
def logs():
    return flask.render_template(
        'failure_log_view.html', context=dict(failure_records=database_engine.all_failure_records()))


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        database_engine.register_program(
            request.form["reg_name"], request.form["reg_filepath"],
            request.form["reg_command"], request.form["reg_author"])
    return redirect(url_for("index"))
