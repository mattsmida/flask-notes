import os

from flask import Flask, render_template, redirect
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User  # BadUser
from forms import CreateUserForm  # LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///hashing_login")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "peanut"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
bcrypt = Bcrypt()


@app.get('/')
def show_homepage():
    """ Show the homepage. """

    return redirect('/register')


@app.method('/register', methods=['GET', 'POST'])
def register_user():

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username
        email = form.email
        first_name = form.first_name
        last_name = form.last_name
        password_hash = bcrypt.generate_password_hash(
            form.password).decode('utf8')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password_hash)

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('register.html')  # TODO: Make register.html