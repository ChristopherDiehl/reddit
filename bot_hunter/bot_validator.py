#template from: /u/GoldenSights
#bot to find all the other bots
import praw
import time
import sqlite3
import datetime
import re
import requests
import traceback
import difflib 
from socket import timeout

'''USER CONFIGURATION'''

APP_ID = ""
APP_SECRET = ""
APP_URI = ""
USERAGENT = "A robot hunter by /u/ShaddiestTerrapin57"
SUBREDDIT = "all"
PRINTFILE = "botNames.txt"
baseComment = ""


try:
   import bot
   APP_ID = bot.APP_ID
   APP_SECRET = bot.APP_SECRET
   APP_URI = bot.APP_URI
   USERAGENT = bot.USERAGENT
except ImportError:
    pass
MAXCOMMENTS = 10
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

print('Loaded Completed table')
sql.commit()

r = praw.Reddit(USERAGENT)
r.set_oauth_app_info(APP_ID, APP_SECRET, APP_URI)


def validate():

    
   try:

      for potentialBot in cur.execute('SELECT * FROM potentialBots'):
      
         print('Validating '+potentialBot[0])
         x = 0
         totalSequentialDiff = 0
         try:
            for comment in r.get_redditor(potentialBot[0]).get_comments(limit=MAXCOMMENTS):
               print(comment)
               if x == 0:
                  baseComment = comment
                  x+=1
                  continue

               seq=difflib.SequenceMatcher(None, baseComment.body,comment.body)
               totalSequentialDiff +=(seq.ratio())


               for block in seq.get_matching_blocks():
                  print("block: ")
                  print(block)
                  print ("a[%d] and b[%d] match for %d elements" % block)

               print (comment.body)

         except praw.errors.NotFound:
            print('user was banned')
            pass

         totalSequentialDiff *= 10
         print(totalSequentialDiff)
         break


   except AttributeError:
      print('AttributeError')
      pass





while True:

   try:
      validate()
   except EOFError:
      print("Error:", e)
   except timeout:
      pass
   except requests.exceptions.RequestException:
      pass

   sql.commit()
   print('Running again in ' + str(WAIT) + ' seconds')
   time.sleep(WAIT)