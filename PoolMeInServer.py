# REST Service for Carpool app

import cherrypy
import pymongo
import PoolMeInProps

from PoolMeInDBHelper import PoolMeInDBHelper
from users import User
from rides import Ride
from search import Search

class Root(object):
    pass

dbHelper= PoolMeInDBHelper()
root = Root()
root.user=User(dbHelper)
root.rides=Ride(dbHelper)
root.rides.search=Search(dbHelper)

conf = {
    'global': {
        'server.socket_host': 'localhost',
        'server.socket_port': 8000,
    },
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
} 
cherrypy.quickstart(root, '/', conf)