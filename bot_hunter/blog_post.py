#template from: /u/GoldenSights
import praw
import time
import traceback
import requests
from socket import timeout

APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "A post condensor by /u/ShaddiestTerrapin57"
SUBREDDIT = "worldnews"
MAXPOSTS = 50
WAIT = 30
#a bot.py file where you list variables
try:
	import bot
	APP_ID = bot.APP_ID
	APP_SECRET = bot.APP_SECRET
	APP_URI = bot.APP_URI
	USERAGENT = bot.USERAGENT
except ImportError:
	pass

#you will need to follow steps found at: http://praw.readthedocs.io/en/stable/pages/oauth.html to setup your bot login
r = praw.Reddit(USERAGENT)
r.set_oauth_app_info(APP_ID, APP_SECRET, APP_URI)

subreddit = r.get_subreddit(SUBREDDIT)
posts = []
posts += subreddit.get_new(limit=MAXPOSTS)


def scanSubreddit():
	try:
		for post in posts:
			url = post.url
			

	except AttributeError:
		print('AttributeError')
		pass


def message(user):
	print('About to message users on '+SUBREDDIT)
	r.send_message(user, 'I am a test bot', 'Awesome Post Man!')



while True:
	try:
		scanSubreddit()

   #handles reddit / local connection instability
	except timeout: 
		pass
	except requests.exceptions.RequestException:
		pass

	print('Running again in ' + str(WAIT) + ' seconds')
	time.sleep(WAIT)



