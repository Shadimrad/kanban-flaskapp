from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Base, User, Board, Task, Contributor


app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)

from app.routes.auth import auth_bp
from app.routes.views import views_bp

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
