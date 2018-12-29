# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:udacity@localhost:5432/catalog'
#DATABASE_CONNECT_OPTIONS = {"check_same_thread=False"}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = 'asd098wer'

# Secret key for signing cookies
SECRET_KEY = 'asd098wer'
