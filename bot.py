# bot.py, an experimentation with Twitter bots
#
# Replies to tweets with a book recommendation fetched via the Oyster API
# based on hashtags contained within the tweet.
#
# by Ian Zapolsky - 3.29.14

import os
import time

import oyster
from twitter import Twitter, OAuth, TwitterHTTPError

# name of the username the bot will operate under
BOT_NAME = 'ianzapolsky'

# Oyster API credentials
OYSTER_ID     = os.environ['OYSTER_ID']
OYSTER_SECRET = os.environ['OYSTER_SECRET']
ACCESS_KEY    = os.environ['ACCESS_KEY']

# Twitter API credentials
OAUTH_TOKEN     = os.environ['OAUTH_TOKEN']
OAUTH_SECRET    = os.environ['OAUTH_SECRET']
CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# return all tweets mentioning @BOT_NAME that have been created since latest_id
def fetch_unseen_mentions(latest_id):
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', since_id=latest_id)['statuses']

# return the id of the latest tweet mentioning @BOT_NAME
def fetch_latest_id():
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', count=1)['statuses'][0]['id']

# convert hashtags dict into a space-separated string
def tags_to_string(hashtags):
  tag_list = ''
  for tag in hashtags:
    tag_list += split_on_caps(tag['text'])+' '
  return tag_list

# split a string if it contains capital letters
def split_on_caps(string):
  result = ''
  for i in range(len(string)):
    # check if a letter is upper case
    if (ord(string[i]) - ord('A')) < 26 and i > 0:
      return string[:i]+' '+split_on_caps(string[i:])
  return string


if __name__ == '__main__':

  # initialize Twitter connection
  t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET))

  # initialize Oyster connection
  auth = oyster.auth.OysterOAuthHandler(
    client_id     = OYSTER_ID,
    client_secret = OYSTER_SECRET,
    oauth_host    = 'api.oysterbooks.com'
  )
  auth.access_token = ACCESS_KEY
  o = oyster.API(
    auth_handler = auth,
    host         = 'api.oysterbooks.com',
  )

  # initialize latest_id to the most recent mention of @BOT_NAME
  latest_id = fetch_latest_id()

  # infinite loop to continously reply to new, properly formatted tweets
  while True:

    print 'waking up!'
    results = fetch_unseen_mentions(latest_id)
    count = 0

    if not results:
      print 'no new tweets.'
    else:
      for tweet in reversed(results):

        tweeter  = tweet['user']['screen_name']
        hashtags = tweet['entities']['hashtags']
        tag_list = tags_to_string(hashtags)

        if tag_list != '':
          # search Oyster API
          try:
            oyster_books = o.book_search(tag_list)
            for book in oyster_books:
              title  = book.title
              author = book.author
              uuid   = book.uuid
              # slug is not a supported field in SimpleBookResource, neither is
              # web_url...
              # slug = book.slug
              # link = 'https://oysterbooks.com/%s/%s' % (uuid,slug)
              msg  = 'Hey @%s! Try "%s" by %s' % (tweeter, title, author)
              if len(msg) <= 140:
                t.statuses.update(status=msg)
                count += 1
                break
          except:
            t.statuses.update(
              status="Hey @"+tweeter+"! We coudn't find any matches for those hashtags. Sorry!")
            count += 1

        latest_id = tweet['id']

    # sleep 60 seconds at the end of each loop to avoid going over API
    # restrictions (180 per 15-minute-window in 1.1)
    print 'replied to '+str(count)+' tweets!'
    print 'going to sleep...'
    time.sleep(30)

