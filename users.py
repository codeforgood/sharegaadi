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
        self.userCol.remove({PoolMeInProps.FIELD_USERNAME:userName})
            
    def _update_user(self, userName):
        self._remove_user(userName)
        self._add_user()
    
    def _find_user(self, userName):
        return self.userCol.find_one({PoolMeInProps.FIELD_USERNAME:userName})
    
    def _build_user_map(self, user):
        self.user_out[PoolMeInProps.FIELD_USERNAME]=user[PoolMeInProps.FIELD_USERNAME]
        self.user_out[PoolMeInProps.FIELD_EMAIL]=user[PoolMeInProps.FIELD_EMAIL]
        self.user_out[PoolMeInProps.FIELD_VEHICLES]=user[PoolMeInProps.FIELD_VEHICLES]
        self.user_out[PoolMeInProps.FIELD_AGE]=user[PoolMeInProps.FIELD_AGE]
        self.user_out[PoolMeInProps.FIELD_SEX]=user[PoolMeInProps.FIELD_SEX]
        self.user_out[PoolMeInProps.FIELD_ADDRESS]=user[PoolMeInProps.FIELD_ADDRESS]
        self.user_out[PoolMeInProps.FIELD_LICENSED]=user[PoolMeInProps.FIELD_LICENSED]
        self.user_out[PoolMeInProps.FIELD_CONTACT]=user[PoolMeInProps.FIELD_CONTACT]
        self.user_out[PoolMeInProps.FIELD_PREFERRED]=user[PoolMeInProps.FIELD_PREFERRED]
                   
    def _authenticate_user(self,user):        
        if(user[PoolMeInProps.FIELD_PASSWORD] == self.user_in[PoolMeInProps.FIELD_PASSWORD]):
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