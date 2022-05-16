import os
import pihole.helpers as pihole_helpers
# Statement for enabling the development environment
DEBUG = False
# WEBSERVER PORT
PORT = 8888
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_BINDS = {
    'pihole': 'sqlite:///' + pihole_helpers.get_database_file()
}
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "8bdeee308efb2c13f58ad5167acd4652"

# Secret key for signing cookies
SECRET_KEY = "cde1ae1a87d3a2b8560174fa7e77ca20"
