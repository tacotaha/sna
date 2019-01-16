#!/usr/bin/env python3

import os
import sys
import time
import tweepy
from credentials import *


class User:
    """
    Twitter user interface. Stores username and maintains
    a local cache of the user's friends and followers.
    """

    def __init__(self, username):
        self.username = username
        self.friends = []
        self.followers = []
        self.mentioned_users = {}
        self.favorited_users = {}
        self.friend_cache = None
        self.follower_cache = None
        self.mentioned_cache = None
        self.favorited_cache = None
        self.datapath = os.path.abspath("data/{}".format(self.username))
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)

    def get_friends(self, cache=True):
        """
        Return friends from local cache if possible,
        o.w. fetch friends via the twitter API
        """
        if self.friend_cache is None or not cache:
            fname = "friends.csv".format(self.username)
            filepath = os.path.join(self.datapath, fname)
            self.friends = self.__fetch(api.friends, filepath)
        return self.friends

    def get_followers(self, cache=True):
        """
        Return followers from local cache if possible,
        o.w. fetch followers via the twitter API
        """
        if self.follower_cache is None or not cache:
            fname = "followers.csv".format(self.username)
            filepath = os.path.join(self.datapath, fname)
            self.followers = self.__fetch(api.followers, filepath)
        return self.followers

    def get_mentions(self, cache=True):
        """
        Return a list of tuples (x, y) where
        x = a username
        y = the # of times they were mentioned by the current user
        """
        if self.mentioned_cache is None or not cache:
            fname = "mentions.csv".format(self.username)
            filepath = os.path.join(self.datapath, fname)
            users = {}
            for status in tweepy.Cursor(api.user_timeline, screen_name=self.username).items():
                if hasattr(status, "entities"):
                    for e in status.entities["user_mentions"]:
                        if e["screen_name"] not in users:
                            users[e["screen_name"]] = 1
                        else:
                            users[e["screen_name"]] += 1
            self.mentioned_users = sorted(users.items(), key=lambda x: int(x[1]), reverse=True)
            with open(filepath, "w") as outfile:
                for (user, frequency) in self.mentioned_users:
                    outfile.write("{},{}\n".format(user, frequency))
        return self.mentioned_users

    def get_favorites(self, count=1000, cache=True):
        """
        Return a list of tuples (x, y) where
        x = a username
        y = the # of favorited tweets authored by user x
        """
        if self.favorited_cache is None or not cache:
            fname = "favorites.csv".format(self.username)
            filepath = os.path.join(self.datapath, fname)
            users = {}
            try:
                for status in tweepy.Cursor(api.favorites, screen_name=self.username, count=count).items():
                    screen_name = status.user.screen_name
                    if screen_name not in users:
                        users[screen_name] = 1
                    else:
                        users[screen_name] += 1
            except tweepy.TweepError:
                print("Rate limited...leaving with %d favorites" % len(users))
            self.favorited_users = sorted(users.items(), key=lambda x: int(x[1]), reverse=True)
            with open(filepath, "w") as outfile:
                for (user, frequency) in self.favorited_users:
                    outfile.write("{},{}\n".format(user, frequency))
        return self.favorited_users

    def __fetch(self, api_attr, out_file_path, count=200):
        """
        Retrieves specified payload from the twiter API
        """
        users = []
        for user in tweepy.Cursor(api_attr, screen_name=self.username, count=count).pages():
            users.extend(user)
        users = [users[i].screen_name for i in range(len(users))]
        with open(out_file_path, "w") as of:
            for user in users:
                of.write("{}\n".format(user))
        return users
