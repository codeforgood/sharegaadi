import cherrypy
import pymongo
import PoolMeInProps

from PoolMeInDBHelper import PoolMeInDBHelper

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

    def PUT(self, *vpath, **params):
        return cherrypy.request.body.read()