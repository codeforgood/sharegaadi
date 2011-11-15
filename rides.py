#  Find rides near:             GET - http://localhost:8000/rides/near?lat=50&lon=30&radius=100
#  Find rides owned by name:    GET - http://localhost:8000/rides/owner?name=saddy

import pymongo
import PoolMeInProps
import json
import cherrypy
from PoolMeInDBHelper import PoolMeInDBHelper

class Ride(object):
    exposed = True
    
    def __init__(self, dbHelper):
        self.postsCol= dbHelper.getCollectionRef(PoolMeInProps.REMOTE_COL_POSTS)
        self.ride_in = None
        self.ride_out = {}
    
    def _validate_param(self, paramMap, param):
        if (param in paramMap.keys()):
               return 1
        return 0
    
    def _get_owner(self, owner):
        print "Reached here"
        ownerdoc = self.postsCol.find_one({"owner":owner})
        result = {"owner":ownerdoc["owner"], "source":ownerdoc["source"], "destin":ownerdoc["destin"]}
        return json.dumps(result)
        
    def _find_rides_near(self, lat, lon, radius):
        x=int(lat)
        y=int(lon)
        r=int(radius)
        print "Find near one"
        ridesNearLocation = self.postsCol.find({"location": {"$within": {"$center": [[x, y], r]}}})
        ridesList = []
        for ride in ridesNearLocation :
             result = {"owner":ride["owner"], "source":ride["source"], "destin":ride["destin"]}                
             ridesList.append(result)
        return json.dumps(ridesList)

    def _add_ride(self):
        self.postsCol.insert(self.ride_in)

    def _add_user(self):
        self.postsCol.insert(self.ride_in)

    def POST(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v

        if vpath:
            if (vpath[0] == "rides"):                  
                self.ride_in=json.loads(cherrypy.request.body.read())
                if (self.ride_in == None):
                    raise cherrypy.HTTPError(500,"something went wrong")
                print self.ride_in
                self.postsCol.insert(self.ride_in)
                cherrypy.response.headers["Content-Type"] = "application/json"
                cherrypy.response.status = 404
                return json.dumps(self.ride_in)
                
    def GET(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v
            
        if vpath:
            if (vpath[0] == "near"):
                self._validate_param(paramMap, "lat")
                self._validate_param(paramMap, "lon")
                self._validate_param(paramMap, "radius")
                ridesNearLocation = self._find_rides_near(paramMap["lat"], paramMap["lon"], paramMap["radius"])
                return ridesNearLocation
            if (vpath[0] == "owner"):
                self._validate_param(paramMap, "name")
                return self._get_owner(paramMap["name"])
