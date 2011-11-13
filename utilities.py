import json

#please add all common utility functions across the project here.
#I will be soon adding a json encoding and decoding classes for posts and user document jsons
#this way we can avoid hardcoding document column names in code anywhere else

class Utility:

    @staticmethod
    def getRide(rideDocument):
        return {"owner":rideDocument["owner"], "route":rideDocument["route"]}