# imports sqlite 
import sqlite3
# imports the date.time package
from datetime import datetime
# imports click, Click is a simple Python module inspired by the stdlib optparse to make writing command line scripts fun. Unlike other modules, it's based around a simple API that does not come with too much magic and is composable.
import click
# imports 'g' from the flask module; 'g' is a special object that is unique for each request; 'current_app' is another special object that points to the Flask application handling the request
from flask import current_app, g
# get_db function
def get_db():
    if 'db' not in g:
        # establishes a connection to the file pointed at by the DATABASE configuration key.
        g.db = sqlite3.connect(
            # retrieves the database path from the Flask application's configuration.
            current_app.config['DATABASE'],
            # enables detection of data types when fetching rows.
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return row that be have like dicts. This allows accessing the columns by name
        g.db.row_factory = sqlite3.Row
    # returns the database connection.
    return g.db

# checks if a connection was created by checking if g.db was set; If the connection exists, it is closed.
def close_db(e=None):
    # retrieves the database connection from 'g' and removes it; default is None if not found.
    db = g.pop('db', None)
    # checks if a database connection exists.
    if db is not None:
        # closes the database connection.
        db.close() 

# init_db function; Initializes the database by running the schema SQL script.
def init_db():
    # gets the database connection.
    db = get_db()
    # open_resource() opens a file relative to the flaskr package.
    with current_app.open_resource('schema.sql') as f:
        # executes the SQL commands from the schema file to set up the database.
        db.executescript(f.read().decode('utf8'))
# click.command() defines a command line command called 'init-db' that calls the init_db function and shows a success message to the user
@click.command('init-db')
# init_db_command function; Clears the existing data and creates new tables.
def init_db_command():
    # calls the init_db function to initialize the database.
    init_db()
    # displays a success message to the user.
    click.echo('Initialized the database.')
# sqlite3.register_converter() tells Python how to interpret timestamp values in the database; the vaslue is then converted to datetime.datetime.
sqlite3.register_converter(
    # specifies the type name in the database ('timestamp') and a function to convert it to datetime
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# init_app function,takes the init_app application and does the registration.
def init_app(app):
    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # app.cli.add_command() adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)


