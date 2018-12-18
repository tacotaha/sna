#!/usr/bin/env python3

import tweepy
from credentials import *

def get_followers(api, twitter_account, num_followers=100):
    followers = []
    page_count = 0

    users = tweepy.Cursor(api.followers, screen_name=twitter_account).items()

    while(len(followers) < num_followers):
        try:
            user = next(users)
        except tweepy.RateLimitError:
            print("RateLimitError...going sleeping for now")
            time.sleep(1000)
            continue

        page_count += 1
        #print("Fetching followers from page {}".format(page_count))
        followers.append(user.screen_name)
    return followers

if __name__ == "__main__":
   followers = get_followers(api, "linux")
   print(followers)
