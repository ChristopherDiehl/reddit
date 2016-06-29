#template from: /u/GoldenSights
import praw
import time
import traceback
from socket import timeout
from bs4 import BeautifulSoup
import requests
import random
import time
#username = Peribot
#password = PeribotPwd
APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "An flirter by /u/ShaddiestTerrapin57"
SUBREDDIT = "stevenuniverse"
MAXPOSTS = 20
WAIT = 30
FLIRT_MESSAGES= ["I got yo numbah!","Hey there Lazuli ;)","I love Stevens Universe!","Hey Lazuli :)"]
refresh_token ='58989266-aQBoF4gHodFL2FHJrNLK0LYDtJw'
BOT ="Lapis_Mirror"
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
r.refresh_access_information(refresh_token)
subreddit = r.get_subreddit(SUBREDDIT)
posts = []
userToReplyTo = r.get_redditor(BOT)
posts += userToReplyTo.get_submitted(limit=MAXPOSTS)




def scanSubreddit():
	
	try:	
		for post in posts:
			
			post_comment(post,FLIRT_MESSAGES[random.randint(0,3 )])

			parsedArticle = ""
			#post_comment(post,parsedArticle)

	except AttributeError:
		print('AttributeError: ')
		traceback.print_exc()
		pass

def post_comment(post, comment):
	post.add_comment(comment)



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



