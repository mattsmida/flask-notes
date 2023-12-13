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
db.create_all()   # This doesn't need to run every time! Could go in a seed.py
                  # and/or just run this in ipython once.

toolbar = DebugToolbarExtension(app)
bcrypt = Bcrypt()


@app.get('/')
def show_homepage():
    """ Show the homepage. """

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """showing and procesing form to register user"""

    # TODO:
    # Check to see whether logged in, and if so, send to user page.
    # (See if username is in the session, which is not just a flask/py thing.)

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        # Have a class method on the model to register the user
        # e.g., username.register(), defined in model
        # ...which returns an instance of the user.

        user = User(
            username=username,
            email=email,
            first_name=first_name,    # See Tuesday notes for an example
            last_name=last_name,      # (class method in User for this:)
            password=password_hash)   # All of this should also be done in m.py

        session["username"] = username

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def log_in_user():
    """ showing and processing login form"""
    # Needs to have a redirect to the user info page if logged in. TODO:

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <-- This is good! More.

        if user:
            session["username"] = user.username
            return redirect(f'/users/{username}')

        else:
            flash('username or password is incorrect')
            return render_template('login.html', form=form)

    # Will only run if v_o_s() returns False, so get rid of the *else*.
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

    # Just pass user over, then in the template, do user.email, user.fname etc
    # ...But is it a security risk to pass user over to the template?
    # No, it's not because user.password will give the hashed password
    # which is already hard to get into because you'd need to get into the
    # backend.

    return render_template('user_info.html', form=form, user_info=user_info)


# Logout should be near login here in the code. Why? Logical grouping of rtes.
@app.post('/logout')
def logout():
    """ Log out the current user and redirect to the root route. """
    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove username if present, but no errors if it isn't
        session.pop('username', None)

    return redirect('/')
