#  REST URI
#  To update details of existing user:      PUT     	- http://localhost:8000/user/[username] with user authentication and other details json
#  To authenticate or add a new user:       POST    	- http://localhost:8000/user/[username] with user authentication and other details json
#  To remove a  user:                       DELETE    	- http://localhost:8000/user/[username] with user authentication

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
        self.user_in=None
        self.user_out={}
    
    def _validate_param(self, paramMap, param):
        if (param in paramMap.keys()):
               return 1
        return 0
    
    def _add_user(self):
        self.userCol.insert(self.user_in)
    
    def _remove_user(self, userName):
        self.userCol.remove({"username":userName})
            
    def _update_user(self, userName):
        self._remove_user(userName)
        self._add_user()
    
    def _find_user(self, userName):
        return self.userCol.find_one({"username":userName})
    
    def _build_user_map(self, user):
        self.user_out["username"]=user["username"]
        self.user_out["email"]=user["email"]
        self.user_out["vehicles"]=user["vehicles"]
        self.user_out["age"]=user["age"]
        self.user_out["sex"]=user["sex"]
        self.user_out["address"]=user["address"]
        self.user_out["licensedtoDrive"]=user["licensedtoDrive"]
        self.user_out["phoneNumber"]=user["phoneNumber"]
        self.user_out["bestwayToReach"]=user["bestwayToReach"]
                   
    def _authenticate_user(self,user):        
        if(user["password"] == self.user_in["password"]):
            self._build_user_map(user)
            return True
        return False
    
    def POST(self, *vpath, **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v
        
        self.user_in=json.loads(cherrypy.request.body.read())
        user=self._find_user(vpath[0])
        if user is None:
            self._add_user()
        else:
            is_auth = self._authenticate_user(user)
        
        cherrypy.response.headers["Content-Type"] = "application/json"
        if (user is None):
            cherrypy.response.status = 200
            return
        else:
            if (is_auth):
                return json.dumps(self.user_out)
            else:
                raise cherrypy.HTTPError(401,"Unauthorized Access")

    def PUT(self, *vpath, **params):        
        paramMap = {}
        for k,v in params.items():
           paramMap[k] = v        
        
        self.user_in=json.loads(cherrypy.request.body.read())
        
        user=self._find_user(vpath[0])        
        if user is None:
            raise cherrypy.HTTPError(404,"User Not Found")
        else:
            is_auth = self._authenticate_user(user)
        
        if (is_auth):
            self._update_user(vpath[0])
            cherrypy.response.status = 200
            return
        else:
            raise cherrypy.HTTPError(401,"Unauthorized Access")                
        
    def DELETE(self, *vpath , **params):
        paramMap = {}
        for k,v in params.items():
            paramMap[k] = v                               
        
        user=self._find_user(vpath[0])        
        if user is None:
            raise cherrypy.HTTPError(404,"User Not Found")                
        else:
            self._remove_user(vpath[0])
            cherrypy.response.status = 200
            cherrypy.response.message = "User removed from PoolMeIn system"
            return       