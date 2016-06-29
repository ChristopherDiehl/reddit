#template from: /u/GoldenSights
import praw
import time
import traceback
from socket import timeout
from bs4 import BeautifulSoup
import io

APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "An example bot by /u/ShaddiestTerrapin57"
SUBREDDIT = "worldnews"
MAXPOSTS = 2
WAIT = 30
START_MESSAGE = "I am a bot. Here is the content: \n"

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
		x = 0
		for post in posts:
			url = post.url
			if str(url).find('https://www.reddit.com') == -1:
				webpage = requests.get(url)
				soup = BeautifulSoup(webpage.content,'html5lib')	
				parsedArticle = ''

				print('url: '+url)
				for p_tag in soup.find_all('p'):
					parsedArticle += str(p_tag.get_text())

				print(parsedArticle +'\n\n')

			parsedArticle = ""
			#post_comment(post,parsedArticle)

	except AttributeError:
		print('AttributeError: ')
		traceback.print_exc()
		pass

def post_comment(post, parsedArticle):
	post.add_comment(START_MESSAGE + parsedArticle)
	print('Comment posted: '+ parsedArticle)



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



