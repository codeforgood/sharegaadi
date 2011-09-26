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
                
    def GET(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v
            
        if vpath:
            if (vpath[0] == "near"):
                self._validate_param(paramMap, "x")
                self._validate_param(paramMap, "y")
                self._validate_param(paramMap, "r")
                posts_nearme = self._find_near(paramMap["x"], paramMap["y"], paramMap["r"])
                result= ""
                for post in posts_nearme:
                    result = result + str(post)
                return result
            if (vpath[0] == "get"):
                self._validate_param(paramMap, "owner")
                return self._get_owner(paramMap["owner"])
                
