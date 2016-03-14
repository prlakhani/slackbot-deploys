'''
A quick script to fetch the id of a channel you want to use.

USAGE: python fetchChannelId.py <channel_name>
'''

import requests
import sys
import os
import json

def get_channels():

    # Environment variables must be set with your tokens
    USER_TOKEN_STRING =  os.environ['SLACK_USER_TOKEN_STRING']
    URL_TOKEN_STRING =  os.environ['SLACK_URL_TOKEN_STRING']

    HASH = "%23"

    params = {"token": USER_TOKEN_STRING }

    # Capture Response as JSON
    response = requests.get("https://slack.com/api/channels.list", params=params)
    channels = json.loads(response.text, encoding='utf-8')["channels"]
    
    return channels


def fetch_id(searchChannel):
    channels = get_channels()
    for channel in channels:
        if channel["name"] == searchChannel:
            return channel["id"]


if __name__ == "__main__":
    channels = get_channels()
    searchChannel = sys.argv[1]
    for channel in channels:
        if channel["name"] == searchChannel:
            print(channel["id"])
            break
