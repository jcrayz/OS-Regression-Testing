import flask
from flask_sqlalchemy import SQLAlchemy
import flask_migrate
from allamericanregress import config
import random
import alembic
import logging
# for editing DB entries
import os
logger = logging.getLogger(__name__)
# hack to get a reference to the templates directory within the package
tmpl_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')

#  ========== Flask App ==========
app = flask.Flask(__name__, static_url_path='/static')
# auto reload template engine when template files change
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = str(int(random.random() * 100000000000))
# set the database location and protocol
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DB_PATH}'
# initialize SQLAlchemy engine
db = SQLAlchemy(app)
# initialize migration engine
migrate = flask_migrate.Migrate(app, db)

# initialize db with flask_migrate
with app.app_context():
    try:
        flask_migrate.init(config.ALEMBIC_PATH)
    except alembic.util.exc.CommandError as e:
        logger.debug('flask db init failed: %s',
                     e)
        raise e
    try:
        flask_migrate.upgrade(config.ALEMBIC_PATH)
    except Exception as e:
        logger.debug('flask db upgrade failed: %s', e)
        raise e
