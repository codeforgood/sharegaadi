
## Property file to specify all static details and Database related fields
## There will not be reference the DB column names anywhere in application 
## apart from this place.


#DB credentials
REMOTE_DB_HOST = 'dbh13.mongolab.com'
REMOTE_DB_PORT = 27137
REMOTE_DB_USER = 'pooladmin'
REMOTE_DB_PASS = 'admin123'

#Collection Details
REMOTE_COL_USERS = 'pool_users'
REMOTE_COL_POSTS = 'carpool_posts'

#Collection field Details

#users collection
FIELD_USERNAME = 'username'
FIELD_PASSWORD= 'password'
FIELD_EMAIL='email'
FIELD_VEHICLES='vehicles'
FIELD_AGE='age'
FIELD_SEX='sex'
FIELD_ADDRESS='address'
FIELD_LICENSED='licensedtoDrive'
FIELD_CONTACT='phoneNumber'
FIELD_PREFERRED='bestwayToReach'