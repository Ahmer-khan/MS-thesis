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
        retweeters_list = []
        for tweet in tweets:
            try:
                tweet_dict = ast.literal_eval(tweet)
                retweeters = tweet_dict["all_retweeters"]
                for id in retweeters:
                    if not id in retweeters_list :
                        retweeters_list.append(id)
                        with open(#path,"a") as f:
                            print(id, file=f)
                            f.close()
            except SyntaxError:
                counter = 0
                while True:
                    index = tweet[counter:].find("}")
                    if index != -1:
                        tweet_slice_dict = tweet[counter:index + 1+counter]
                        tweet_dict = ast.literal_eval(tweet_slice_dict)
                        retweeters = tweet_dict["all_retweeters"]
                        for id in retweeters:
                            if not id in retweeters_list :
                                retweeters_list.append(id)
                                with open(#path,"a") as f:
                                    print(id, file=f)
                                    f.close()
                        counter = index + 1 + counter
                    else:
                        break
        tweets.close()
        print("-----------")
print("completed")
