from twython import Twython, TwythonRateLimitError, TwythonError
import os
import time
import ast
import json
API_Key = "XAcYNqLwHyhSvXrXBBjNH28Yc"
API_Secret = "Ji7tRpBT73peMSGrBYkOqAvxGCcu5KqM5pjtBFE9ywysbAiX0n"
Access_Token = "307878227-5O8g0wQTxjS6E647rsYNKSvhr21jK7T2mxCKnscr"
Access_Token_Secret = "gIAKx7YR2q1Srbxk8cgNejfweVsepDHZZUhXJB1MlZAdi"
twitter_final = Twython(API_Key, API_Secret,
                  Access_Token, Access_Token_Secret)
trends = []
path = ""
for(path, dir, files) in os.walk("first half"):
    trends.extend(dir)
    break
stop = len(trends)//2 + 1
for i in range(stop,len(trends)):
        print("---------------------------------------------------")
        print("Starting for trend : ", trends[i])
        tweets = open(path + "/" + trends[i] + "/tweets_list.txt","r")
        list_tweet_dict = []
        for tweet in tweets:
            tweet_dict = {}
            tweet = tweet.replace("{","")
            tweet = tweet.replace("}","")
            index = tweet.find(":")
            tweet_dict["tweet_id"] = tweet[1:index-1]
            tweet = tweet[index + 2:]
            tweet = tweet.replace("'","")
            tweet = tweet.replace(" ","")
            tweet = tweet.replace("\n","")
            tweet = tweet.split(",")
            for entry in tweet:
                sep = entry.find(":")
                key = entry[0:sep]
                value = entry[sep + 1:]
                tweet_dict[key] = value
            list_tweet_dict.append(tweet_dict)
        count_retweets = []
        for dict in list_tweet_dict:
            if int(dict["retweets"]) > 0 :
                count_retweets.append(dict)
        total_to_be_processed = len(count_retweets)
        print("Total Tweets : ", total_to_be_processed)
        tweets.close()
        #tweets = open(path + "/" + trend + "/tweets_list.txt","r")
        retweets_file = open(path + "/" + trends[i] + "/retweets.txt", 'r')
        total_done = len(retweets_file.readlines())
        retweets_file.close()
        retweets_file = open(path + "/" + trends[i] + "/retweets.txt", 'a')
        print("Total Tweets Completed : ", total_done)
        line_no_for_tweets = 0
        for line_dict in count_retweets:
            #line = line.decode("utf-8")
            if (line_no_for_tweets > total_done):
                print("Processing Tweet : ", line_no_for_tweets,
                      "/", total_to_be_processed)
                # print("Line Dict Value :", line_dict)
                retweet_dict = {}
                retweet_dict["all_retweeters"] = []
                retweet_dict["tweet id"] = line_dict["tweet_id"]
                retweet_dict["user"] = line_dict["user"]
                retweet_dict["name"] = line_dict["fullname"]
                retweet_dict["tweet time"] = line_dict["timestamp"]
                retweet_dict["retweet count"] = line_dict["retweets"]
                next_cursor = -1
                try:
                    while next_cursor != 0 :
                        retweeters_element = twitter_final.get_retweeters_ids(id = line_dict["tweet_id"], cursor = next_cursor)
                        retweet_dict["all_retweeters"].extend(retweeters_element["ids"])
                        next_cursor = retweeters_element["next_cursor"]
                        retweets_file.write(json.dumps(retweet_dict))
                        retweets_file.write('\n')
                except TwythonRateLimitError as error:
                    remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    del twitter_final
                    if remainder > 0:
                        time.sleep(remainder)
                    else:
                        remainder *= -1
                        time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    line_no_for_tweets -= 1
                    continue
                except TwythonError as e:
                    if e.error_code == 403:
                        retweets_file.write(json.dumps(retweet_dict))
                        continue
                    #else:
                        #retweets_file.write(json.dumps(rettweet_dict))
                        #retweets_file.write('\n')
            line_no_for_tweets += 1
        tweets.close()
        retweets_file.close()
        print("---------------------------------------------------")
        print('')
