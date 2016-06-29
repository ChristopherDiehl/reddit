#template from: /u/GoldenSights
#copy of autotldr
#need to have installed praw,sumy
import praw
import time
import traceback
import requests
from socket import timeout
from bs4 import BeautifulSoup
import sumy.summarizers.lsa as lsa_module
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.utils import get_stop_words
import io

MAX_SENTENCES = 2
APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "An autotldr copy by /u/ShaddiestTerrapin57"
SUBREDDIT = "worldnews"
MAXPOSTS = 30
WAIT = 160
START_MESSAGE = "I am a bot. I was able to reduce article to 4 sentences: \n"
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
			#url = post.url
			print('post ['+str(x)+']')
			url = 'http://www.bbc.com/news/world-europe-36658187'

			if str(url).find('https://www.reddit.com') == -1:
				webpage = requests.get(url)
				soup = BeautifulSoup(webpage.content,'html5lib')			
				parsedArticle = ''

				for p_tag in soup.find_all('p'):
					parsedArticle += str(p_tag.get_text())

				print(parsedArticle)
				print('\nvs\n')

				print('parsedArticle :' +parsedArticle)
				post_comment(post,parsedArticle)

	except AttributeError:
		print('AttributeError')
		pass

def local_summarize(articleToSummarize) :

	summarizer = LsaSummarizer()
	summarizer.stopwords = get_stop_words('ENGLISH')
	return summarizer(articleToSummarize, MAX_SENTENCES)

def post_comment(post, parsedArticle):
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



