import flask
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from allamericanregress import config, models, database_engine

# hack to get a reference to the templates directory within the package
import os

tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')

#  ========== Flask App ==========
app = flask.Flask(__name__, static_url_path='/static')
# auto reload template engine when template files change
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
# set the database location and protocol
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DB_PATH}'
# initialize SQLAlchemy engine
db = SQLAlchemy(app)
# initialize migration engine
migrate = Migrate(app, db)


# ========== Routes ==========


@app.route("/")
def index():
    return flask.render_template(
        'index.html',
        context=dict(
            message="Welcome!", programs=list(models.Program.query.all())))


@app.route("/logs")
def logs():
    return flask.render_template(
        'log_view.html', context=dict(logs=models.Log.query.all()))


@app.route("/home")
def home():
    return flask.render_template(
        'mockup.html', context=dict(registrants=models.Program.query.all()))


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        database_engine.register_program(request.form["reg_name"], request.form["reg_filepath"],
                                         request.form["reg_command"])
    return redirect(url_for('home'))


# ========== Utility Functions ==========


def serve():
    print('serving webapp')
    app.run(debug=True)
