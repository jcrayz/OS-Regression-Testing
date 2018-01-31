import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from allamericanregress import config
from allamericanregress import models
# hack to get a reference to the templates directory within the package
import os
tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')

#  ========== Flask App ==========
app = flask.Flask(__name__)
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
    return flask.render_template('mockup.html', context=dict())


# ========== Utility Functions ==========


def serve():
    print('serving webapp')
    app.run(debug=True)
