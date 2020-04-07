from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['intranet.redbutte.utah.edu', '155.98.238.12']

try:
    from .local import *
except ImportError:
    pass
