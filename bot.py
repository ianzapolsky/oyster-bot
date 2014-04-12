import os
import oyster

OYSTER_ID     = os.environ['OYSTER_ID']
OYSTER_SECRET = os.environ['OYSTER_SECRET']
ACCESS_KEY    = os.environ['ACCESS_KEY']

auth = oyster.auth.OysterOAuthHandler(
    client_id     = OYSTER_ID, 
    client_secret = OYSTER_SECRET,
    oauth_host    = 'api.oysterbooks.com'
)
auth.access_token = ACCESS_KEY

api  = oyster.API(
    auth_handler = auth, 
    host         = 'api.oysterbooks.com',
)

'''
auth = oyster.auth.OysterOAuthHandler(OYSTER_ID, OYSTER_SECRET)
auth.access_token = ACCESS_KEY
api = oyster.API(auth, host='api.oysterbooks.com')
'''

x = api.search('Steinbeck')

print x[0].title

