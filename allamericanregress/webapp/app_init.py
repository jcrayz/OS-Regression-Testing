import flask
from flask_sqlalchemy import SQLAlchemy
import flask_migrate
from allamericanregress import config
import random
import logging
import os
import alembic

logger = logging.getLogger(__name__)
# hack to get a reference to the templates directory within the package
if config.FROZEN:
    tmpl_dir = os.path.join(config.MODULE_PATH, 'templates')
    static_dir = os.path.join(config.MODULE_PATH, 'static')
else:
    tmpl_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates')
    static_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'static')
#  ========== Flask App ==========
app = flask.Flask(__name__, static_url_path='/static',
                  template_folder=tmpl_dir, static_folder=static_dir)
# auto reload template engine when template files change
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = str(int(random.random() * 100000000000))
# set the database location and protocol
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DB_PATH}'
# initialize SQLAlchemy engine
db = SQLAlchemy(app)
# initialize migration engine
migrate = flask_migrate.Migrate(app, db, directory=config.ALEMBIC_PATH)
