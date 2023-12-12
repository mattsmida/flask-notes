import os

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, BadUser
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///hashing_login")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "peanut"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)