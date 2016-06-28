#template from: /u/GoldenSights
#copy of autotldr
#need to have installed praw,sumy
import praw
import time
import traceback
import requests
from socket import timeout
from bs4 import BeautifulSoup
from pytldr.summarize import LsaOzsoy


SENTENCES_COUNT = 6
APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "An autotldr copy by /u/ShaddiestTerrapin57"
SUBREDDIT = "worldnews"
MAXPOSTS = 1
WAIT = 160
START_MESSAGE = "I am a bot. I was able to reduce to 6 sentences: \n"
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
			print(post)
			if url != '':

				webpage = requests.get(url)
				soup = BeautifulSoup(webpage.content,'httml5lib')			
				parsedArticle = ''
				for p_tag in str(soup.p.get_text()):
					parsedArticle += p_tag

				post_comment(post,parsedArticle)



	except AttributeError:
		print('AttributeError')
		pass

def summarize(articleToSummarize) :
	summarizer = LsaOzsoy()
	return summarizer.summarize(articleToSummarize, topics=2, length=SENTENCES_COUNT, binary_matrix=True, topic_sigma_threshold=0.5)

def post_comment(post, parsedArticle):
	parsedArticle = summarize(parsedArticle)
	r.add_comment(START_MESSAGE + parsedArticle)
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



