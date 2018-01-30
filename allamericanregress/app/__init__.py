from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import allamericanregress.config as config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + config.DB_PATH

db = SQLAlchemy(app)
migrate = Migrate(app, db)

