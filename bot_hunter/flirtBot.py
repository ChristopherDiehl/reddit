#template from: /u/GoldenSights
import praw
import time
import traceback
from socket import timeout
from bs4 import BeautifulSoup
import requests
import random
import sqlite3
import time
#username = Peribot
#password = PeribotPwd
APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "An flirter by /u/ShaddiestTerrapin57"
SUBREDDIT = "stevenuniverse"
MAXPOSTS = 30
WAIT = 1028
FLIRT_MESSAGES= ["I got yo numbah!","Hey there Lazuli ;)","I love Stevens Universe!","Hey Lazuli :)"]
refresh_token ='58989266-aQBoF4gHodFL2FHJrNLK0LYDtJw'
BOT_TO_FLIRT_WITH ="Lapis_Mirror"

sql = sqlite3.connect('flirt_comments.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS flirtComments(commentId TEXT)')
sql.commit()

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
#posts += subreddit.get_new(limit=MAXPOSTS)




def scanSubreddit():
	
	try:	
		for post in r.get_redditor(BOT_TO_FLIRT_WITH).get_submitted(limit=MAXPOSTS):
			#print(post.author.name)
			#print(post.title)
			#if post.author.name == BOT_TO_FLIRT_WITH:
			print('Post found')
			postId = post.id
			cur.execute('SELECT * FROM flirtComments WHERE commentId=?', [postId])
			fetched = cur.fetchone()

			if not fetched:
				post_comment(post,FLIRT_MESSAGES[random.randint(0,3 )])
				cur.execute('INSERT INTO flirtComments VALUES(?)', [postId])
				sql.commit()

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



