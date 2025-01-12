# Importing the functools module, which provides higher-order functions that act on or return other functions.
import functools
# Importing various components from Flask to create and manage the application.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# Importing functions for securely hashing and checking passwords.
from werkzeug.security import check_password_hash, generate_password_hash
# Importing the 'get_db' function from the 'flaskr.db' module to interact with the database.
from flaskr.db import get_db
# Creating a Blueprint named 'auth' for authentication-related routes with a URL prefix of '/auth'.
bp = Blueprint('auth', __name__, url_prefix='/auth')
# @bp.route associates the URL /register with the register view function. When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.
@bp.route('/register', methods=('GET', 'POST'))
# register function.
def register():
    # If the user submitted the form, 'request.method' will be 'POST'. In this case, start validating the input
    if request.method == 'POST':
        # 'request.form' is a special type of dict mapping submitted form keys and values. The user will input their username.
        username = request.form['username']
        # 'request.form' is a special type of dict mapping submitted form keys and values. The user will input their username.
        password = request.form['password']
        # Getting a database connection.
        db = get_db()
        # Initializing an error variable to store any validation errors.
        error = None
        # Checking if the username is empty.
        if not username:
            # Setting the error message for a missing username.
            error = 'Username is required.'
        # Checking if the password is empty.
        elif not password:
            # Setting the error message for a missing password.
            error = 'Password is required.'
        # If no validation errors occurred, proceed to register the user.
        if error is None:
            try:
                # db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders with. The database library will take care of escaping the values so you are not vulnerable to a SQL injection attack
                db.execute(
                    # generate_password_hash() is used to securely hash the password, and that hash is stored.
                    (username, generate_password_hash(password)),
                )
                # db.commit() is called after 'db.execute' password hashing to save the changes.
                db.commit()
            # if username already exists, shows validation error to the user.
            except db.IntegrityError:
                # Setting the error message for a duplicate username.
                error = f"User {username} is already registered."
            else:
                # 'url_for()' generates the URL for the login view based on its name; 'redirect()' generates a redirect response to the generated URL.
                return redirect(url_for("auth.login"))   
        # 'flash()' stores messages that can be retrieved when rendering the template, shows an error if validation fails.
        flash(error)
    # 'render_template()' rendering the registration page template if the request method is GET or validation fails.
    return render_template('auth/register.html')
# @bp.route associates the URL /login with the login view function.
@bp.route('/login', methods=('GET', 'POST'))
# Defining the login function to handle user authentication.
def login():
    # Checking if the request method is POST, indicating a form submission.
    if request.method == 'POST':
        # Retrieving the submitted username from the form data.
        username = request.form['username']
        # Retrieving the submitted password from the form data.
        password = request.form['password']
        # Getting a database connection.
        db = get_db()
        # Initializing an error variable to store any validation errors.
        error = None
        # Executing an SQL query to fetch the user with the provided username.
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        # 'fetchone()' returns one row from the query. If the query returned no results, it returns None.
        ).fetchone()
        # Checking if the username exists in the database.
        if user is None:
            # Setting the error message for an incorrect username.
            error = 'Incorrect username.'
        # check_password_hash() hashes the submitted password in the same way as the stored hash and securely compares them. If they match, the password is valid.
        elif not check_password_hash(user['password'], password):
            # Setting the error message for an incorrect password.
            error = 'Incorrect password.'
        # If no validation errors occurred, log in the user.
        if error is None:
            # session is a dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session. The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely signs the data so that it can’t be tampered with.
            session.clear()
            # Storing the logged-in user's ID in the session.
            session['user_id'] = user['id']
            # Redirecting to the index page after successful login.
            return redirect(url_for('index'))
        # Flashing the error message to the user if login fails.
        flash(error)
    # Rendering the login page template if the request method is GET or validation fails.
    return render_template('auth/login.html')
# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
# load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database, storing it on g.user, which lasts for the length of the request. If there is no user id, or if the id doesn’t exist, g.user will be None.
def load_logged_in_user():
    # Retrieving the user ID from the session, if available.
    user_id = session.get('user_id')
    # Checking if no user ID is stored in the session.
    if user_id is None:
        # Setting the global user object to None.
        g.user = None
    else:
        # Fetching the user’s data from the database and storing it in the global user object.
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()   
# To log out, you need to remove the user id from the session. Then 'load_logged_in_user' won’t load a user on subsequent requests.
@bp.route('/logout')
# Defining a function to log out the user by clearing the session.
def logout():
    # Clearing the session data, effectively logging out the user.
    session.clear()
    # Redirecting to the index page after logging out.
    return redirect(url_for('index')) 
# Defining a decorator to restrict access to views that require authentication.
def login_required(view):
    # Using functools.wraps to preserve the original view function's attributes.
    @functools.wraps(view)
    # Defining a wrapped function to enforce login restrictions.
    def wrapped_view(**kwargs):
        # Checking if no user is logged in.
        if g.user is None:
            # 'url_for()' function generates the URL to a view based on a name and arguments.
            return redirect(url_for('auth_login'))
        # Returning the original view function if the user is authenticated.
        return view(**kwargs)
    # Returning the wrapped view function.
    return wrapped_view                    
       