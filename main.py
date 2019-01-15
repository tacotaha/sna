#!/usr/bin/env python

import argparse
from user import User

def main(username, followers, friends, mentions, favorites):
    user = User(username)
    all = not followers and not friends and not mentions and not favorites
    if followers or all:
        user_followers = user.get_followers()
        print("=========={} Followers==========".format(len(user_followers)))
        print(user_followers)
    if friends or all:
        user_friends = user.get_friends()
        print("=========={} Friends============".format(len(user_friends)))
        print(user_friends)
    if mentions or all:
        user_mentions = user.get_mentions()
        print("=========={} Mentioned============".format(len(user_mentions)))
        print(user_mentions)
    if favorites or all:
        user_favorites = user.get_favorites()
        print("=========={} Favorited============".format(len(user_favorites)))
        print(user_favorites)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='A valid Twitter user name')
    parser.add_argument('--followers', action="store_true",
                        help='Fetch the user\'s followers')
    parser.add_argument('--friends', action="store_true",
                        help='Fetch the user\'s friends')
    parser.add_argument('--mentions', action="store_true",
                        help='Fetch a list of mentioned users')
    parser.add_argument('--favorites', action="store_true",
                        help='Fetch a list of the users whose tweets were favorited')
    args = parser.parse_args()
    main(args.username, args.followers, args.friends, args.mentions, args.favorites)
