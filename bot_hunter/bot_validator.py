#template from: /u/GoldenSights
#bot to determine if bot is a bot
#wanted to evaluate average response time, but after investigation realized there was too much variation.
#I believe this variation was due to the irregularities associated with redidt. Ie. tons of post one day, dead the next
#When there are no posts, autotldr and other response bots no longer need to post as frequently

import praw
import time
import sqlite3
import datetime
import re
import requests
import traceback
import difflib 
from socket import timeout
import datetime

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
WAIT = 30

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
         numOfHyperlinksInBaseComment = 0
         sizeOfCommonBlock = 0
         aBlockStart = 0
         commonString = ""
         hyperLinkScore = 10
         commonStringScore = 0

         comments = r.get_redditor(potentialBot[0]).get

         try:

            for comment in r.get_redditor(potentialBot[0]).get_comments(limit=MAXCOMMENTS):
               print(comment)
               print(dir(r.get_redditor(potentialBot[0])))
               if x == 0:
                  baseComment = comment
                  numOfHyperlinksInBaseComment = baseComment.body.count("](http")

                  x +=1

               elif x == 1:
                  seq=difflib.SequenceMatcher(None, baseComment.body,comment.body)
                  totalSequentialDiff +=(seq.ratio())


                  if baseComment.body.count("](http") == numOfHyperlinksInBaseComment:
                     hyperLinkScore += 10


                  for block in seq.get_matching_blocks():
                     if block[2] > sizeOfCommonBlock:
                        sizeOfCommonBlock = block[2]
                        end = int(block[0]+block[2])
                        commonString = comment.body[block[0]:end:]

                  x+=1

               else: 
                  seq=difflib.SequenceMatcher(None, baseComment.body,comment.body)
                  totalSequentialDiff +=(seq.ratio())
                  if baseComment.body.count("](http") == numOfHyperlinksInBaseComment:
                     hyperLinkScore += 10

                  if comment.body.find(commonString) != -1:
                     commonStringScore += 12.5
            
            x = 0
            totalSequentialDiff *= 10
            print("hyperLinkScore: " +str(hyperLinkScore))
            print("totalSequentialDiff: "+str(totalSequentialDiff))
            print(commonString)
            print('commonStringScore: '+str(commonStringScore))
            commonStringScore = 0

         except praw.errors.NotFound:
            print('user was banned')
            pass



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