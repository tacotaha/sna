#!/usr/bin/env python

import argparse
from user import User

def main(username, followers, friends, mentioned):
    user = User(username)
    all = not followers and not friends and not mentioned
    if followers or all:
        user_followers = user.get_followers()
        print("=========={} Followers==========".format(len(user_followers)))
        print(user_followers)
    if friends or all:
        user_friends = user.get_friends()
        print("=========={} Friends============".format(len(user_friends)))
        print(user_friends)
    if mentioned or all:
        user_mentioned = user.get_mentioned()
        print("=========={} Mentioned============".format(len(user_mentioned)))
        print(user_mentioned)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='A valid Twitter user name')
    parser.add_argument('--followers', action="store_true",
                        help='Fetch the user\'s followers')
    parser.add_argument('--friends', action="store_true",
                        help='Fetch the user\'s friends')
    parser.add_argument('--mentioned', action="store_true",
                        help='Fetch a list of mentioned users')
    args = parser.parse_args()
    main(args.username, args.followers, args.friends, args.mentioned)
