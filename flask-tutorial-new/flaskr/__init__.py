# import os module
import os
# import the flask class from flask package 
from flask import Flask

""" Application factory function """ 
# create_app - the application factory function.
def create_app(test_config=None):
    
    # creates the flask instance,  __name__ name of the current python module; instance_relative_config=True tells the app the configuration files are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)
    # sets default configuration that the app will use coming from the flask instance
    app.config.from_mapping(
        # keeps data safe.
        SECRET_KEY='dev',
        # path where the sqlite database will be served; app.instance_path path that Flask has chosen for the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # if statement for test_config
    if test_config is None:
        # overrides the default configuration with values taken from the config.py file in the instance folder 
        app.config.from_pyfile('config.py', silent=True)
    # else statement  
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    # except for try statement 
    except OSError:
      # pass for try statement 
        pass

    # I visit the hello endpoint
    @app.route('/hello')
    # then I call the hello function
    def hello():
        # and return the message in the browser
        return 'Hello, World! My name is Los🐍'
    
    # Imports the db module from the project
    from . import db
    #  init_app registration 
    db.init_app(app)

# Imports the auth module from the project
    from . import auth
# register_blueprint registration 
    app.register_blueprint(auth.bp)

# Imports the blog module from the project
    from . import blog
    app.register_blueprint(blog.bp)
# Register a rule for routing incoming requests and building URLs 
    app.add_url_rule('/', endpoint='index')
#  returns the app 
    return app 
   

