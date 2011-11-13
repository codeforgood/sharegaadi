import PoolMeInProps as PMIP

from pymongo import Connection

class PoolMeInDBHelper(object):
    
    def __init__(self):
        
        if PMIP.DB == "local":    
            self.poolmein_Con = Connection(PMIP.LOCAL_DB_HOST, PMIP.LOCAL_DB_PORT)
            self.poolmein_DB=self.poolmein_Con[PMIP.LOCAL_DB]            
        elif PMIP.DB == "remote":
            self.poolmein_Con = Connection(PMIP.REMOTE_DB_HOST, PMIP.REMOTE_DB_PORT)
            self.poolmein_DB=self.poolmein_Con[PMIP.REMOTE_DB]
            self.poolmein_DB.authenticate(PMIP.REMOTE_DB_USER,PMIP.REMOTE_DB_PASS)
            print "remote"
        else:
            exit(1)
        
    def getCollectionRef(self, collectionName):
        self.colRef=self.poolmein_DB[collectionName]
        return self.colRef