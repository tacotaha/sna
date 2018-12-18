#!/usr/bin/env python3

import os
import time
import tweepy
from credentials import *

class User:
    def __init__(self, username):
        self.username = username
        self.friends = []
        self.followers = []
        self.friend_cache = None
        self.follower_cache = None
        if not os.path.exists(self.username):
            os.mkdir(self.username)
        self.datapath = os.path.abspath("./{}".format(self.username))

    def get_friends(self, cache=True):
        if self.friend_cache is None and not cache:
            self.fetch_friends()
        else:
            return self.friends


    def get_followers(self, cache=True):
        if self.follower_cache is None and not cache:
            self.fetch_followers()
        else:
            return self.followers

    def fetch_friends(self):
        """
        Fetch the user's friends using the twitter API
        """
        friends = []
        users = tweepy.Cursor(api.friends, screen_name=self.username).items()
        timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
        filepath = os.path.join(self.datapath,
                   "{}-friends-{}.txt".format(self.username,timestamp))
        with open(filepath, "w") as outfile:
            while True:
                try:
                    user = next(users)
                except tweepy.RateLimitError:
                    print("RateLimitError...sleeping for now")
                    time.sleep(1000)
                    continue
                except StopIteration:
                    break
                outfile.write("{}\n".format(user.screen_name))
                friends.append(user.screen_name)
        self.friend_cache = timestamp
        self.friends = friends

    def fetch_followers(self):
        """
        Fetch the user's followers using the twitter API
        """
        followers = []
        users = tweepy.Cursor(api.followers, screen_name=self.username).items()
        timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
        filepath = os.path.join(self.datapath,
                   "{}-followers-{}.txt".format(self.username,timestamp))
        with open(filepath, "w") as outfile:
            while True:
                try:
                    user = next(users)
                except tweepy.RateLimitError:
                    print("RateLimitError...sleeping for now")
                    time.sleep(1000)
                    continue
                except StopIteration:
                    break
                followers.append(user.screen_name)
        self.follower_cache = timestamp
        self.followers = followers


if __name__ == "__main__":
    user = User("twitter")
    user.fetch_followers()
    follwers = user.get_followers()
    print(followers)
