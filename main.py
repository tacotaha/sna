#!/usr/bin/env python

import argparse
from user import User

def main(username, followers, friends):
    user = User(username)
    if followers or (not followers and not friends):
        user_followers = user.get_followers()
        print("=========={} Followers==========".format(len(user_followers)))
        print(user_followers)
    if friends or (not followers and not friends):
        user_friends = user.get_friends()
        print("=========={} Friends============".format(len(user_friends)))
        print(user_friends)
   # mentions = user.get_mentions()
   # print(mentions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='A valid Twitter user name')
    parser.add_argument('--followers', action="store_true",
                        help='Fetch the user\'s followers')
    parser.add_argument('--friends', action="store_true",
                        help='Fetch the user\'s friends')
    args = parser.parse_args()
    main(args.username, args.followers, args.friends)
