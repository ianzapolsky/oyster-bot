# OYSTERBOT

### description

Twitter bot that responds to tweets in which it is mentioned with a book
recommendation pulled from the Oyster API based on hashtags contained within
the tweet. Intended to be run as a cron job.

### requirements

This program uses [twitter][twitter], a Python wrapper for the Twitter API, and
the Oyster Python API Client.

### setup

To setup OYSTERBOT on a new machine, first create a Twitter account and 
register it as an application with Read/Write access at dev.twitter.com. 

Then clone this repository to your machine. Copy the username of your Twitter 
account into the BOT\_NAME variable declarations at the top of both bot.py and 
setup.py. 

Create a file called .obrc and add the Oyster Python Client library to your 
PYTHONPATH. Also create environment variables for your Twitter and Oyster API 
authentication keys, following the naming conventions in bot.py.

Logout and login to the machine again, and then finally run setup.py to
initialize the file .latest\_id to the last mention of your Twitter account.

Now, configure cron.sh to reflect the directory where bot.py is located on your
host machine, and add a cron job to run cron.sh every minute (or whatever time
interval you want).

[twitter]:https://github.com/sixohsix/twitter
    

