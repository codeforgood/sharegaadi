#  Find rides near:        GET - http://localhost:8000/rides/near?lat=50&lon=30&radius=100

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

    def _find_near(self, x, y, r):
        x1=int(x)
        y1=int(y)
        r1=int(r)
        return self.postsCol.find({"loc": {"$within": {"$center": [[x1, y1], r1]}}})

    def _get_owner(self, owner):
        print "Reached here"
        ownerdoc = self.postsCol.find_one({"owner":owner})
        return ownerdoc["owner"]+','+ownerdoc["source"]+','+ownerdoc["destin"]
        
    def _find_near_one(self, lat, lon, radius):
        x=int(lat)
        y=int(lon)
        r=int(radius)
        print "Find near one"
        return self.postsCol.find_one({"location": {"$within": {"$center": [[x, y], r]}}})
        
    def GET(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v
            
        if vpath:
            if (vpath[0] == "near"):
                self._validate_param(paramMap, "lat")
                self._validate_param(paramMap, "lon")
                self._validate_param(paramMap, "radius")
                posts_nearme = self._find_near_one(paramMap["lat"], paramMap["lon"], paramMap["radius"])                
                result = {"owner":posts_nearme["owner"], "source":posts_nearme["source"], "destin":posts_nearme["destin"]}                
                return json.dumps(result,indent=4)
