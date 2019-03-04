from webServe import keep_alive
import tweepy
import os
import json
import requests
import datetime
from datetime import tzinfo, timedelta

def madness():
  # Setting time to PST so that scores are retrieved for the correct date
  minus8 = -timedelta(hours=8)

  class PST(tzinfo):
      def utcoffset(self, dt):
          return minus8

      def tzname(self, dt):
          return "PST"

      def dst(self, dt):
          return minus8

  pst = PST()

  now = datetime.datetime.now(pst)

  currentDate = now.strftime("%Y/%m/%d")

  url = "https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/{}/scoreboard.json".format(currentDate)

  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'} 

  response = requests.get(url, headers = headers)

  jsonStr = response.text

  gamesList = json.loads(jsonStr)

  # Tweepy/Twitter API auth stuff
  C_KEY = os.getenv("C_KEY")
  C_SECRET = os.getenv("C_SECRET")
  A_TOKEN = os.getenv("A_TOKEN")
  A_TOKEN_SECRET = os.getenv("A_TOKEN_SECRET")

  auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
  auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
  api = tweepy.API(auth)

  with open('oldGames.txt', 'r') as oldGamesFile:
      oldGamesList = oldGamesFile.read().splitlines()

  # the 'games' key in the JSON document contains a list, so have to parse the list first. it's a list of additionak key-value pairs
  # also to note, Python treats JSON objects as Python dictionaries
  for game in gamesList['games']:
    #'game' variable is actually a Python dictionary object containing key-value pair data for each game
    # we can parse the Py dictionary normally
    #print(game['game']['finalMessage'])

    if game['game']['finalMessage'] == "FINAL" or game['game']['finalMessage'] == "FINAL (OT)":
      thisGameID = game['game']['gameID']
      awayTeam = game['game']['away']['names']['full']
      awayTeamScore = game['game']['away']['score']
      homeTeam = game['game']['home']['names']['full']
      homeTeamScore = game['game']['home']['score']
      

      if thisGameID not in oldGamesList:
        oldGamesList.append(thisGameID)
        api.update_status('Final Score:\n{}: {}\n{}: {}\n\n#collegehoops #ncaaMBB'.format(awayTeam, awayTeamScore, homeTeam, homeTeamScore))
        print("Processed: " + thisGameID)
      
    else:
      print("Game incomplete")

  oldGamesFile.close()

  oldGamesFile = open('oldGames.txt', 'w')
  for oldGamesListItem in oldGamesList:
    oldGamesFile.write('{}\n'.format(oldGamesListItem))
  oldGamesFile.close()

  return("Tweeted scores successfully.")

  '''
  Additional Features:
  - Check for finished games every minute
  - Erase oldGames.txt file at beginning of each day
  '''

keep_alive()
