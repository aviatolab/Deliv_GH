from flask import Flask


from app.config import Config
from app.models import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

from app.views import *

if __name__ == '__main__':
    app.run()
