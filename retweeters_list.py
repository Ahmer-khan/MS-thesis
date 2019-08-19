import os
trends = []
path = ""
for(path, dir, files) in os.walk(#path):
    trends.extend(dir)
    break
for trend in trends:
        #new_dir = os.path.join(path, name)
        #file = os.listdir(new_dir)
        #retweets_file = open(path)
        #retweets_file.close()
        tweets = open(#path)
        retweeters_list = []
        for tweet in tweets:
            tweet = tweet.replace("{","")
            tweet = tweet.replace("}","")
            tweet = tweet.replace("[","")
            tweet = tweet.replace("]","")
            index = tweet.find(":")
            tweet = tweet.replace('"',"")
            tweet = tweet.replace(" ","")
            tweet = tweet.replace("\n","")
            stop = tweet.find("tweetid")
            retweeters =  tweet[index + 1 : stop - 1]
            retweeters = retweeters.split(",")
            for id in retweeters:
                if not id in retweeters_list :
                    retweeters_list.append(id)
                    with open(#path) as f:
                        print(id, file=f)
                f.close()
        tweets.close()

