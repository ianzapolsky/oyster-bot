# setup.py

# This script should be run once when setting up a twitter bot that uses an
# outside textfile .latest_id to store id of the last seen tweet. 

# by Ian Zapolsky

import os

from twitter import Twitter, OAuth, TwitterHTTPError

# twitter username for bot 
BOT_NAME = 'ianzapolsky'

# Twitter API credentials
OAUTH_TOKEN     = os.environ['OAUTH_TOKEN']
OAUTH_SECRET    = os.environ['OAUTH_SECRET']
CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# return the id of the latest tweet mentioning @BOT_NAME
def fetch_latest_id():
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', count=1)['statuses'][0]['id']

if __name__ == '__main__':
  
  # initialize Twitter connection
  t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET))

  latest_id = str(fetch_latest_id())

  # write the latest_id to the file .latest_id
  f = open('.latest_id', 'w')
  f.write(latest_id)
  f.close()
