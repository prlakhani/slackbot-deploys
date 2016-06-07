import random
import time
import requests
import json
import csv
import os
from random import shuffle
import pickle
import os.path
import datetime
import pytz
import fetchChannelId as fci

from User import User

# Environment variables must be set with your tokens
USER_TOKEN_STRING =  os.environ['SLACK_USER_TOKEN_STRING']
URL_TOKEN_STRING =  os.environ['SLACK_URL_TOKEN_STRING']

HASH = "%23"


# Configuration values to be set in setConfiguration
class Bot:
    def __init__(self):
        self.setConfiguration()

        self.csv_filename = "log" + time.strftime("%Y%m%d-%H%M") + ".csv"
        # local cache of usernames
        # maps userIds to usernames
        self.user_cache = self.loadUserCache()

        # round robin store
        self.user_queue = []


    def loadUserCache(self):
        if os.path.isfile('user_cache.save'):
            with open('user_cache.save','rb') as f:
                self.user_cache = pickle.load(f)
                print("Loading " + str(len(self.user_cache)) + " users from cache.")
                return self.user_cache

        return {}

    '''
    Sets the configuration file.

    Runs after every callout so that settings can be changed realtime
    '''
    def setConfiguration(self):
        # Read variables fromt the configuration file
        with open('config.json') as f:
            settings = json.load(f)

            self.team_domain = settings["teamDomain"]
            self.channel_name = settings["channel"]
            self.deploy_time = settings["callouts"]["deployTime"]
            self.num_people_per_callout = settings["callouts"]["numPeople"]
            self.sliding_window_size = settings["callouts"]["slidingWindowSize"]
            # self.channel_id = settings["channelId"]
            self.channel_id = fci.fetch_id(settings["channel"])
            self.timezone = pytz.timezone(settings["timezone"])
            self.office_hours_on = settings["officeHours"]["on"]
            self.office_hours_begin = settings["officeHours"]["begin"]
            self.office_hours_end = settings["officeHours"]["end"]
            self.no_weekends = settings["officeHours"]["noWeekends"]
            self.allowed_to_deploy = settings["allowedToDeploy"]
            self.debug = settings["debug"]

        self.post_URL = "https://" + self.team_domain + ".slack.com/services/hooks/slackbot?token=" + URL_TOKEN_STRING + "&channel=" + HASH + self.channel_name

################################################################################
'''
Selects an active user from a list of users
'''
def selectUser(bot):
    active_users = fetchActiveUsers(bot)

    # Add all active users not already in the user queue
    # Shuffles to randomly add new active users
    shuffle(active_users)
    bothArrays = set(active_users).intersection(bot.user_queue)
    for user in active_users:
        if user not in bothArrays:
            bot.user_queue.append(user)

    # The max number of users we are willing to look forward
    # to try and find a good match
    sliding_window = bot.sliding_window_size

    # find a user to draw, priority going to first in
    for i in range(len(bot.user_queue)):
        user = bot.user_queue[i]

        # TODO: add responsibility balancing over the course of a week
        if user in active_users:
            # Decrease sliding window by one. Basically, we don't want to jump
            # too far ahead in our queue
            sliding_window -= 1
            if sliding_window <= 0:
                break

    # If everybody has done exercises or we didn't find a person within our sliding window,
    for user in bot.user_queue:
        if user in active_users:
            bot.user_queue.remove(user)
            return user

    # If we weren't able to select one, just pick a random
    print("Selecting user at random (queue length was " + str(len(bot.user_queue)) + ")")
    return active_users[random.randrange(0, len(active_users))]


'''
Fetches a list of all active users in the channel
'''
def fetchActiveUsers(bot):
    # Check for new members
    # params = {"token": USER_TOKEN_STRING, "channel": bot.channel_id}
    # response = requests.get("https://slack.com/api/channels.info", params=params)
    # user_ids = json.loads(response.text, encoding='utf-8')["channel"]["members"]
    user_ids = bot.allowed_to_deploy
    active_users = []

    for user_id in user_ids:
        # Add user to the cache if not already
        if user_id not in bot.user_cache:
            bot.user_cache[user_id] = User(user_id)

        if bot.user_cache[user_id].isActive():
            active_users.append(bot.user_cache[user_id])

    return active_users


'''
Selects a person to do the already-selected exercise
'''

def main():
    bot = Bot()
    bot.setConfiguration()
    winner_announcement = "please deploy to Heroku!"
    winner = selectUser(bot)
    winner_list = 'Captain '
    winner_list += str(winner.getUserHandle().decode()) + ': ' # remove b'
    winner_announcement = winner_list + winner_announcement
    # Announce the user if it's a weekday
    if not bot.debug:
        if not bot.no_weekends:
            requests.post(bot.post_URL, data=winner_announcement)
        elif datetime.date.today().weekday() < 5:
            requests.post(bot.post_URL, data=winner_announcement)
        else:
            print("It's a weekend, no deploys!")
    else:
        print(winner_announcement)

main()
