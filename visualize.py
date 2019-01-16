import os
from user import User
import networkx as nx
import matplotlib.pyplot as plt

"""
Uses networkx to create various social graphs along with matplotlib for
visualizing them.
"""

class Visualize:
    def __init__(self, username):
        self.username = username
        self.followers = list()
        self.following = list()
        self.mentions = list()
        self.favorites = list()
        datapath = os.path.join("data", self.username)
        # Check data path for previously generated data
        if os.path.exists(datapath):
            followers_file = os.path.join(datapath, "followers.csv")
            following_file = os.path.join(datapath, "friends.csv")
            mentions_file = os.path.join(datapath, "mentions.csv")
            favorites_file = os.path.join(datapath, "favorites.csv")
            if os.path.exists(followers_file):
                with open(followers_file, "r") as ff:
                    for line in ff.readlines():
                        self.followers.append(line.strip())
            if os.path.exists(following_file):
                with open(following_file, "r") as ff:
                    for line in ff.readlines():
                        self.following.append(line.strip())
            if os.path.exists(mentions_file):
                with open(mentions_file, "r") as mf:
                    for line in mf.readlines():
                        line = line.strip()
                        user, freq = line.split(",")
                        self.mentions.append((user, int(freq)))
            if os.path.exists(favorites_file):
                with open(favorites_file, "r") as ff:
                    for line in ff.readlines():
                        line = line.strip()
                        user, freq = line.split(",")
                        self.favorites.append((user, int(freq)))

        # Otherwise, generate it from twitter 
        if not self.followers and not self.following and not self.mentions and not self.favorites:
            print("Local data not found. Reaching out to Twitter...")
            user = User(self.username)
            self.followers = user.get_followers()
            self.following = user.get_friends()
            self.mentions = user.get_mentions()
            self.favorites = user.get_favorites()

    def get_follow_graph(self, count=50):
        self.follow_graph = nx.DiGraph()
        self.follow_graph.add_node(self.username)
        top_followers = self.get_top_followers_by_favorites()
        top_following = self.get_top_following_by_favorites()

        for follower in top_followers[:count]:
            self.follow_graph.add_edge(self.username, follower)
            if follower in self.following:
                self.follow_graph.add_edge(follower, self.username)

        for friend in self.following[:count]:
            if friend not in top_followers:
                self.follow_graph.add_edge(friend, self.username)

        return self.follow_graph

    def get_top_followers_by_favorites(self):
        res = list()
        for user,freq in self.favorites:
            if user in self.followers:
                res.append(user)
        return res

    def get_top_followers_by_mentions(self):
        res = list()
        for user,freq in self.mentions:
            if user in self.followers:
                res.append(user)
        return res

    def get_top_following_by_favorites(self):
        res = list()
        for user,freq in self.favorites:
            if user in self.following:
                res.append(user)
        return res

    def get_top_following_by_mentions(self):
        res = list()
        for user,freq in self.mentions:
            if user in self.following:
                res.append(user)
        return res
