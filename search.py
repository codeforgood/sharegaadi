#  Find rides near:        GET - http://localhost:8000/rides/search/near?lat=50&lon=30&(limit=10)
#  Find rides within:      GET - http://localhost:8000/rides/search/within?lat=50&lon=30&radius=100&(limit=10)
#  Find rides with tags:   GET - http://localhost:8000/rides/search/tags?tag=men&tag=doordrop

import cherrypy
import pymongo
import PoolMeInProps
import json

from utilities import Utility
from PoolMeInDBHelper import PoolMeInDBHelper

class Search(object):
    exposed = True
    
    def __init__(self, dbHelper):
        self.postsCol= dbHelper.getCollectionRef(PoolMeInProps.REMOTE_COL_POSTS)
    
    def _validate_param(self, param):
        if (param in self.paramMap.keys()):
            return True
        return False
    
    def _find_with_tags(self, tags):
        rideDocs = self.postsCol.find({"Tags":{"$in":tags}})
        return rideDocs
    
    def _find_within_circle(self, lat, lon, radius, n=10):
        x=float(lat)
        y=float(lon)
        degree=float(float(radius) / (PoolMeInProps.EARTH_RADIUS_KM))
        n=int(n)
        rideDocs = self.postsCol.find({"location":{"$within":{"$center":[[x, y], degree]}}}).limit(n)
        return rideDocs
    
    def _find_near(self, lat, lon, n=10):
        x=float(lat)
        y=float(lon)
        n=int(n)
        print n
        rideDocs = self.postsCol.find({"location": {"$near": [x, y]}}).limit(n)
        return rideDocs
    
    def GET(self, *vpath, **params):
        self.paramMap = {}
        for k,v in params.items():
            self.paramMap[k] = v
        
        ridesList = []
        cherrypy.response.headers["Content-Type"] = "application/json"    
        if vpath:
            if (vpath[0] == "near"):
                if not (self._validate_param("lat") and self._validate_param("lon")):
                    cherrypy.response.status = 400
                    return json.dumps({"Error":True,"Message":PoolMeInProps.REQUEST_PARAM_MISSING})
                
                if (self.paramMap.has_key("limit")):                    
                    rideDocs = self._find_near(self.paramMap["lat"], self.paramMap["lon"], self.paramMap["limit"])
                else:
                    rideDocs = self._find_near(self.paramMap["lat"], self.paramMap["lon"])
            elif(vpath[0] == "within"):
                if not (self._validate_param("lat") and self._validate_param("lon") and self._validate_param("radius")):
                    cherrypy.response.status = 400
                    return json.dumps({"Error":True,"Message":PoolMeInProps.REQUEST_PARAM_MISSING})
                
                if (self.paramMap.has_key("limit")):                    
                    rideDocs = self._find_within_circle(self.paramMap["lat"], self.paramMap["lon"], self.paramMap["radius"], self.paramMap["limit"])
                else:
                    rideDocs = self._find_within_circle(self.paramMap["lat"], self.paramMap["lon"], self.paramMap["radius"])
            elif(vpath[0] == "tags"):
                if not (self._validate_param("tag")):
                    cherrypy.response.status = 400
                    return json.dumps({"Error":True,"Message":PoolMeInProps.REQUEST_PARAM_MISSING})
                else:
                    rideDocs = self._find_with_tags(self.paramMap["tag"])
            else:
                cherrypy.response.status = 400
                return json.dumps({"Error":True,"Message":PoolMeInProps.INVALID_URI})
                
            for rideDoc in rideDocs :
                result = Utility.getRide(rideDoc)               
                ridesList.append(result)
            return json.dumps(ridesList);