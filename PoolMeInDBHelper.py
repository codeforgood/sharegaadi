import PoolMeInProps

from pymongo import Connection

class PoolMeInDBHelper(object):
    
    def __init__(self):
        self.poolmein_Con = Connection(PoolMeInProps.REMOTE_DB_HOST, PoolMeInProps.REMOTE_DB_PORT)
        self.poolmein_DB=self.poolmein_Con.poolmeindb
        self.poolmein_DB.authenticate(PoolMeInProps.REMOTE_DB_USER,PoolMeInProps.REMOTE_DB_PASS)
        
    def getCollectionRef(self, collectionName):
        self.colRef=self.poolmein_DB[collectionName]
        return self.colRef