import os
import pickle
from user import User
import networkx as nx
import matplotlib.pyplot as plt

"""
Uses networkx to create various social graphs along with matplotlib for
visualizing them.
"""

class Graph:
    """
    Generates social graphs given a directory of users
    """
    def __init__(self, path="data"):
        self.path = path
        self.users = list()
        self.followers = dict()
        self.following = dict()
        self.favorites = dict()
        self.mentions = dict()
        for user in os.listdir(path):
            print(user)
            self.users.append(user)
            userpath = os.path.join(path, user)
            followers_path = os.path.join(userpath, "followers.pkl")
            following_path = os.path.join(userpath, "friends.pkl")
            favorites_path = os.path.join(userpath, "favorites.pkl")
            mentions_path = os.path.join(userpath, "mentions.pkl")
            assert(os.path.exists(followers_path))
            assert(os.path.exists(following_path))
            assert(os.path.exists(favorites_path))
            assert(os.path.exists(mentions_path))
            with open(followers_path, "rb") as f:
                self.followers[user] = pickle.load(f)
            with open(following_path, "rb") as f:
                self.following[user] = pickle.load(f)
            with open(favorites_path, "rb") as f:
                self.favorites[user] = pickle.load(f)
            with open(mentions_path, "rb") as f:
                self.mentions[user] = pickle.load(f)

    def get_follow_graph(self, max_users=10, count=10):
        self.follow_graph = nx.DiGraph()
        for user in self.users[:max_users]:
            self.follow_graph.add_node(user)
            for follower in self.followers[user][:count]:
                self.follow_graph.add_edge(follower, user)
            for friend in self.following[user][:count]:
                self.follow_graph.add_edge(user, friend)
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

if __name__ == "__main__":
    graph = Graph()
    g = graph.get_follow_graph()
    with open("graph.pkl", "wb") as f:
            pickle.dump(self.follow_graph, f)
    pos = nx.spring_layout(g, scale=20)
#    nx.draw(g, pos, font_size=3, with_labels=True)
    nx.draw(g, pos, node_size=60, dpi=1000)
    plt.savefig("output.png", dpi=1000)
    plt.savefig("output.pdf")
