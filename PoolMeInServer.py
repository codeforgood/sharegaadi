# REST Service for Carpool app
# URI: 
#  To Check for user presence: http://localhost:8000/user?username=tim
#  To Add a new user:          http://localhost:8000/user/add?username=tim&password=abcd1234
#  To authenticate user:       http://localhost:8000/user/auth?username=tim&password=abcd1234
#  Find posts near:			   http://localhost:8000/posts/near?x=50&y=50&r=50

import cherrypy
import pymongo
import PoolMeInProps

from PoolMeInDBHelper import PoolMeInDBHelper
from pymongo import Connection

class User(object):

    exposed = True
    
    def __init__(self, dbHelper):
        self.userCol= dbHelper.getCollectionRef(PoolMeInProps.REMOTE_COL_USERS)
    
    def _validate_param(self, paramMap, param):
        if (param in paramMap.keys()):
               return 1
        return 0
    
    def _add_user(self, user_name, password):
        self.userCol.insert({"username":user_name, "password":password})
        
    
    def _find_user(self, user_name):
        return self.userCol.find_one({"username":user_name})
    
    def _authenticate_user(self, user_name,password):
        user = self.userCol.find_one({"username":user_name})
        if(user["password"] == password):
            return True
        return False
    
    def GET(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v
            
        if vpath:
            if (vpath[0] == "add"):
                self._validate_param(paramMap, "username")
                self._validate_param(paramMap, "password")
                self._add_user(paramMap["username"], paramMap["password"])
                return "User "+paramMap["username"] + " Added Successfully"
                
            elif (vpath[0] == "auth"):
                self._validate_param(paramMap, "username")
                self._validate_param(paramMap, "password")
                is_auth = self._authenticate_user(paramMap["username"], paramMap["password"])
                if is_auth:
                    return "Authorized User"
                else:
                    return "User Not Authorized"
            else:
                return "Invalid URL Request"
        
        user = self._find_user(paramMap["username"])
        if user is None:
            return "User Not Found"
        else:
            return "User Exists"

    def PUT(self):
        pass

class Posts(object):
    exposed = True
    
    def __init__(self):
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
        
    
class Root(object):
    pass

dbHelper= PoolMeInDBHelper()
root = Root()
root.user=User(dbHelper)
root.posts=Posts()

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