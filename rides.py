# Post a ride
# Delete a ride
# Update a ride
# Get a ride detail

import cherrypy
import pymongo
import PoolMeInProps
import json

from PoolMeInDBHelper import PoolMeInDBHelper

class Ride(object):
    exposed = True
    
    def __init__(self, dbHelper):
        self.postsCol= dbHelper.getCollectionRef(PoolMeInProps.REMOTE_COL_POSTS)
    
    def _validate_param(self, paramMap, param):
        if (param in paramMap.keys()):
               return 1
        return 0
                
    def GET(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v		
		#to be implemented