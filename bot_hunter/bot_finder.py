#template from: /u/GoldenSights
#bot to find all the other bots
import praw
import time
import sqlite3
import datetime
import re
import requests
import traceback
from socket import timeout

'''USER CONFIGURATION'''

APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "A robot hunter by /u/ShaddiestTerrapin57"
SUBREDDIT = "all"
PRINTFILE = "botNames.txt"

try:
    import bot
    APP_ID = bot.APP_ID
    APP_SECRET = bot.APP_SECRET
    APP_URI = bot.APP_URI
    USERAGENT = bot.USERAGENT
except ImportError:
    pass
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

WAITS = str(WAIT)
lastwikiupdate = 0

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS potentialBots(NAME TEXT)')
print('Loaded Completed table')
sql.commit()

r = praw.Reddit(USERAGENT)
r.set_oauth_app_info(APP_ID, APP_SECRET, APP_URI)


def scan():
    print('Scanning ' + SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = []
    posts += subreddit.get_new(limit=MAXPOSTS)
    posts += subreddit.get_comments(limit=MAXPOSTS)
    try:
        for post in posts:
            pauthor = post.author.name
            match = re.search(r'((?i)b)(ot)', pauthor)
            if match:
                cur.execute('SELECT * FROM potentialBots WHERE NAME=?', [pauthor])
                fetched = cur.fetchone()
                if not fetched:
                    cur.execute('INSERT INTO potentialBots VALUES(?)', [pauthor])
                    print(pauthor+': inserted into db')

                sql.commit()

    except AttributeError:
        print('AttributeError')
        pass



while True:
    try:
        scan()
    except EOFError:
        print("Error:", e)
    except timeout:
        pass
    except requests.exceptions.RequestException:
        pass

    sql.commit()
    print('Running again in ' + str(WAIT) + ' seconds')
    time.sleep(WAIT)