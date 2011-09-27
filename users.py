# URI: 
#  To Add a new user:          PUT - http://localhost:8000/user/add?username=tim
#  To authenticate user:       GET - http://localhost:8000/user/auth?username=tim&password=abcd1234

import cherrypy
import pymongo
import PoolMeInProps
import json

from PoolMeInDBHelper import PoolMeInDBHelper
from utilities import Utility

class User(object):

    exposed = True
    
    def __init__(self, dbHelper):
        self.userCol= dbHelper.getCollectionRef(PoolMeInProps.REMOTE_COL_USERS)
        self.user=None
    
    def _validate_param(self, paramMap, param):
        if (param in paramMap.keys()):
               return 1
        return 0
    
    def _add_user(self):
        #self.userCol.insert({"username": "saddy","password": "xd45l3mf9"})
        print json.dumps(self.user)
        self.userCol.insert(self.user)
            
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
            if (vpath[0] == "auth"):
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
        self.user=json.loads(cherrypy.request.body.read())
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v        
        if vpath:
            if (vpath[0] == "add"):
                self._validate_param(paramMap, "username")
                self._add_user()
                
        userName=paramMap["username"]
        result={userName:True}
        
        return json.dumps(result)