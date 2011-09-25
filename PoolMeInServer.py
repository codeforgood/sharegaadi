# REST Service for Carpool app
# URI: 
#  To Check for user presence: http://localhost:8000/user?username=tim
#  To Add a new user:          http://localhost:8000/user/add?username=tim&password=abcd1234
#  To authenticate user:       http://localhost:8000/user/auth?username=tim&password=abcd1234
#  Find rides near:			   http://localhost:8000/rides/near?x=50&y=50&r=50

import cherrypy
import pymongo
import PoolMeInProps

from PoolMeInDBHelper import PoolMeInDBHelper
from users import User
from rides import Ride

class Root(object):
    pass

dbHelper= PoolMeInDBHelper()
root = Root()
root.user=User(dbHelper)
root.rides=Ride(dbHelper)

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