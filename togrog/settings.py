import os

from jinja2 import Environment, FileSystemLoader
from togrog import templatefilters

ASYNC = True
if os.environ.get('TOGROG_ASYNC_OFF'):
    ASYNC = False
    
if ASYNC:
    print "Doing ASYNC"
    import txmongo as backend
    connectionclass = backend.MongoConnection
else:
    print "Doing SYNC"
    import pymongo as backend
    backend.ObjectId = backend.objectid.ObjectId
    connectionclass = backend.connection.Connection
    
STATIC_PATH = "./static"
TEMPLATE_PATH = "./template"
LOGIN_URL = "/login"
COOKIE_SECRET = "IZ9xTGsAT6+5BAlZHwMAin3CQKYXeEcptQjjP8XBeJk="
APP_NAME = "togrog"
APP_PORT = 9000
APP_INTERFACE = "0.0.0.0"

def get_connection():
    connection = connectionclass()
    return connection
    
def get_database():
    database = getattr(get_connection(), APP_NAME)
    return database

TEMPLATE_FILTERS = {
    "timesince": templatefilters.timesince,
    "timeuntil": templatefilters.timeuntil,
}

def url_mappings():
    import handlers
    return [
        (r"/", handlers.IndexHandler),
        (r"/login/?", handlers.AuthHandler),
    ]
    
    
def setup_environment():
    e = Environment(
        loader=FileSystemLoader(TEMPLATE_PATH),
        autoescape=True,
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.i18n']
    )
    e.filters.update(TEMPLATE_FILTERS)
    
    return e
    