import os

from flask import Flask, render_template, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User  # BadUser
from forms import CreateUserForm, LoginUserForm, CSRFProtectForm

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


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """showing and procesing form to register user"""

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')

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
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def log_in_user():
    """ showing and processing login form"""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{username}')

        else:
            flash('username or password is incorrect')
            return render_template('login.html', form=form)

    else:
        return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user_info(username):
    """ Show information about the current user only if logged in. """

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    user_info = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    return render_template('user_info.html', form=form, user_info=user_info)


@app.post('/logout')
def logout():
    """ Log out the current user and redirect to the root route. """
    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove username if present, but no errors if it isn't
        session.pop('username', None)

    return redirect('/')
