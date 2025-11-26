# server/extensions.py
# This file centralizes extensions so they can be imported cleanly

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()      # Main database instance
migrate = Migrate()    # Migration manager