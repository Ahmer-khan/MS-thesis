import os
import ast
trends = []
path = ""
for(path, dir, files) in os.walk(#path):
    trends.extend(dir)
    break
for trend in trends:
        print("---------")
        print("starting for trend:",trend)
        tweets = open(#path,"r")
        tweeters_list = []
        for tweet in tweets:
            try:
                tweet_dict = ast.literal_eval(tweet)
                tweeter = tweet_dict["user"]
                if not tweeter in tweeters_list :
                    tweeters_list.append(tweeter)
                    with open(#path,"a") as f:
                        print(tweeter, file=f)
                        f.close()
            except SyntaxError:
                counter = 0
                while True:
                    index = tweet[counter:].find("}")
                    if index != -1:
                        tweet_slice_dict = tweet[counter:index + 1+counter]
                        tweet_dict = ast.literal_eval(tweet_slice_dict)
                        tweeter = tweet_dict["user"]
                        if not tweeter in tweeters_list :
                            tweeters_list.append(tweeter)
                            with open(#path,"a") as f:
                                print(tweeter, file=f)
                                f.close()
                        counter = index + 1 + counter
                    else:
                        break
        tweets.close()
        print("-----------")
print("completed")
