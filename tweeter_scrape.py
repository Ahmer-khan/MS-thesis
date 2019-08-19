from twython import Twython, TwythonRateLimitError, TwythonError
import os
import time
import csv
from datetime import datetime
API_Key = ""
API_Secret = ""
Access_Token = ""
Access_Token_Secret = ""
twitter_final = Twython(API_Key, API_Secret,
                  Access_Token, Access_Token_Secret)
trends = []
path = ""
for (path,dir,file) in os.walk(#path):
    trends.extend(dir)
    break
for q in range(0,6):
    print("---------------------------------------------------")
    print("starting for trends[q]:",trend)
    users = []
    if not os.path.exists(#path):
	    os.mkdir(#path)
    f = open(#path)
    users = f.readlines()
    try:
        with open(#path) as f1:
            user_done = f1.readlines()
            f1.close()
    except FileNotFoundError:
        user_done = []
    print("Total users:",len(users))
    print("user remaining:",len(users) - len(user_done))
    if len(user_done) == 0:
        resume = 0
    else:
        resume = len(user_done)
    for i in range(resume,len(users)):
        print('***************************')
        print("Scraping user:",str(i+1) + "/" + str(len(users)))
        username = users[i]
        if not os.path.exists(#path):
            os.mkdir(#path)
	    alltweets = []
        new_tweets = []
        try:
		    with open(#path) as re:
                rows = csv.reader(re,delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    new_tweets.append(row)
                re.close()
            total = len(new_tweets)
            oldest = int(new_tweets[-1][0]) - 1
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(new_tweets[-1][1],'%a %b %d %H:%M:%S +0000 %Y'))
            print ("...%s tweets downloaded so far" % (total))
        except FileNotFoundError:
            try:
                new_tweets = twitter_final.get_user_timeline(screen_name = username,count = 200,include_rts='true')
                alltweets.extend(new_tweets)
            except TwythonRateLimitError as error:
                remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                del twitter_final
                if remainder > 0:
                    time.sleep(remainder)
                else:
                    remainder *= -1
                    time.sleep(remainder)
                twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                new_tweets = twitter_final.get_user_timeline(screen_name = username,count=200,include_rts='true')
                alltweets.extend(new_tweets)
            except TwythonError as e:
                if e.error_code != 503 and e.error_code != 500:
                    try:
                        with open(#path) as fp :
                            print(username,file=fp)
                            fp.close()
                    except FileNotFoundError:
                        with open(#path) as fp :
                            print(username,file=fp)
                            fp.close()
                    continue
                else:
                    remainder = float(twitter_final.get_lastfunction_header(header='retry-after')) - time.time()
                    del twitter_final
                    if remainder > 0:
					    time.sleep(remainder)
                    else:
                        remainder *= -1
                        time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    new_tweets = twitter_final.get_user_timeline(screen_name = username,count=200,include_rts='true')
                    alltweets.extend(new_tweets)
			total = len(alltweets)
            oldest = alltweets[-1]["id"] - 1
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(alltweets[-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            print ("...%s tweets downloaded so far" % (total))
        ts = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
        stop_date = datetime.strptime('2017-01-01','%Y-%m-%d')
        while ts.year >= stop_date.year and len(new_tweets) > 0:
                del new_tweets [:]
                print("getting tweets before %s" % (oldest))
                try:
                    new_tweets = twitter_final.get_user_timeline(screen_name = username,count=200,max_id=oldest,include_rts='true')
                except TwythonRateLimitError as error:
                    remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    del twitter_final
                    if remainder > 0:
                        time.sleep(remainder)
                    else:
                        remainder *= -1
                        time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    new_tweets = twitter_final.get_user_timeline(screen_name = username,count=200,max_id=oldest)
                except TwythonError as e:
                    if e.error_code == 500 or e.error_code == 503 :
                        remainder = float(twitter_final.get_lastfunction_header(header='retry-after')) - time.time()
                        del twitter_final
                        if remainder > 0:
                            time.sleep(remainder)
                        else:
                            remainder *= -1
                            time.sleep(remainder)
                        twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                        new_tweets = twitter_final.get_user_timeline(screen_name = username,count=200,max_id=oldest)
                alltweets.extend(new_tweets)
                total += len(new_tweets)
                oldest = alltweets[-1]["id"] - 1
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(alltweets[-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
                ts = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
                print(len(new_tweets))
                print ("...%s tweets downloaded so far" % (total))
        try:
            outtweets = [[tweet['id_str'], tweet['created_at'], tweet['text'].encode("utf-8"),tweet['retweeted_status']["user"]["screen_name"]]
                        for tweet in alltweets]
        except KeyError:
            outtweets = [[tweet['id_str'], tweet['created_at'], tweet['text'].encode("utf-8"),tweet["user"]["screen_name"]]
                        for tweet in alltweets]
        try:
            ap = open(#path)
            writer = csv.writer(ap)
            writer.writerows(outtweets)
            ap.close()
        except FileNotFoundError:
            with open(#path, 'w') as ap:
                writer = csv.writer(ap)
                writer.writerows(["id","created_at","text","original_user"])
                writer.writerows(outtweets)
                ap.close()
        try:
            with open(#path,"a") as fp :
                print(username,file=fp)
                fp.close()
        except FileNotFoundError:
            with open(path + "/" + trends[q] + "/tweeters/user_done.txt","w") as fp :
                print(username,file=fp)
                fp.close()
        print("---------------------------------------------------")
        print('')
print("completed")
