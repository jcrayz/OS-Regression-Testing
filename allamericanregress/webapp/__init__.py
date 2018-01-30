import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from allamericanregress import config
# hack to get a reference to the templates directory within the package
import os
tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')

#  ========== Flask App ==========
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DB_PATH}'
# initialize SQLAlchemy engine
db = SQLAlchemy(app)
# initialize migration engine
migrate = Migrate(app, db)


# ========== Routes ==========


@app.route("/")
def index():
    return flask.render_template(
        'index.html', context=dict(message="Welcome!"))


@app.route("/logs")
def logs():
    return flask.render_template(
        'log_view.html')

# ========== Utility Functions ==========


def serve():
    print('serving webapp')
    app.run(debug=True)
