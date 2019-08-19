import tweepy  # https://github.com/tweepy/tweepy
import csv
from pymongo import MongoClient
#from twitter import *

import subprocess
import sys
import json

client = MongoClient()

db = client.twitter_data

users = db['users']

tweets = db.tweets

friends = db.friends

db_retweets = db.retweets

followers = db.followers

distinct_followers = db.followers.distinct('screen_name')

followers_retweets = db.followers_retweets2

# Twitter API credentials
consumer_key = "q9fR004pShLQg39uGKM10NEhW"
consumer_secret = "oHE3g6XVflASZBwk8T9XulxDYWCb9VXBII64g0yEoKX0TzmKwE"
access_key = "1539432170-KCcGaltseUMEfJjbRJvSj0IGcohT0SK3i10h6id"
access_secret = "wzhSxH7EJUg7WGJzbsAQfWk31dx78MfF2ZpixltqNCE8M"


def get_all_tweets(screen_name):

    print("screen_name : %s" % screen_name)
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    # new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    new_tweets = api.retweets()

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    print("alltweets length : %d" % len(alltweets))
    if len(alltweets) > 0:
        oldest = alltweets[-1].id - 1

    # write the csv
    # with open('%s_tweets.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["screen_name", "len(alltweets)"])
    #     writer.writerows([screen_name, str(len(alltweets))])
    #
    # pass

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, include_rts='true')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print
        "...%s tweets downloaded so far" % (len(alltweets))
        # db.followers_retweets.insertMany([alltweets])
    # transform the tweepy tweets into a 2D array that will populate the csv
    for tweet in alltweets:
        # followers_tweet = tweet  # [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")]]

        followers_retweets.insert_one(tweet._json)
        # print(tweet)


if __name__ == '__main__':

    # print(distinct_followers)

    # itr = 4416
    itr = 129468
    print("starting from iteration " + str(itr))
    curr_user = ''

    for i in range(itr, len(distinct_followers)):
        # print(distinct_followers[i])
        try:
            with open('tweetnumber2.txt', 'a') as m:
                m.write(str(i) + ", " + str(distinct_followers[i]) + "\n")
                itr = i
                # awriter.writerow([str(i)])
                get_all_tweets(distinct_followers[i])   # pass in the username of the account you want to download
        except Exception as e:
            print("Ecxeption occurred: " + str(e))
            with open('tweetstatus.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([itr, str(distinct_followers[itr]), str(e)])
                itr = itr + 1
            # if not m.closed:
            #     m.flush()
            #     m.close()

        pass

    #     followers_collection.update({"d_id": tweet[0]}, tweet, True)

