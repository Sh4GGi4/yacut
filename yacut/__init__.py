from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
app.json.ensure_ascii = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
from .models import URLMap


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'URLMap': URLMap}
