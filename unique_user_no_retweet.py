import os
import ast
trends = []
path = ""
for(path, dir, files) in os.walk(#path):
    trends.extend(dir)
    break
for i in range(0,len(trends)):
        print("---------------------------------------------------")
        print("Starting for trend : ", trends[i])
        tweets = open(#path ,"r")
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
            if int(dict["retweets"]) == 0 :
                count_retweets.append(dict)
        total_to_be_processed = len(count_retweets)
        print("Total Tweets : ", total_to_be_processed)
        tweets.close()
        tweets = open(#path,"r")
        user_file = open(#path, 'r')
        total_done = len(user_file.readlines())
        user_list = []
        for user in user_file :
            print(user)
            user_list.append(user)
            print(user_list)
        user_file.close()
        user_file = open(#path, 'a')
        print("Total user found", total_done)
        line_no_for_tweets = 0
        for line in count_retweets:
            if total_to_be_processed != 0:
                print(user_list)
                print(line["user"])
                print(line["user"] in user_list)
                break
                    #print("Processing Tweet : ", line_no_for_tweets,
                          #"/", total_to_be_processed)
                    #print(line["user"])
                    #user_final = line["user"]
                    #print(user_final)
                    #user_file.write(user_final)
                    #user_file.write('\n')
                    #line_no_for_tweets += 1
                #else :
                    #print("Processing Tweet : ", line_no_for_tweets,
                          #"/", total_to_be_processed, "already found")
                    #line_no_for_tweets += 1
            else:
                print("no tweets")
                break
        break
        tweets.close()
        user_file.close()
        print("---------------------------------------------------")
        print('')

