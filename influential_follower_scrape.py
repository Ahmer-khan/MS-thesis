from twython import Twython, TwythonRateLimitError,TwythonError
import os
import time
import csv
from datetime import datetime
import pandas as pd
API_Key = ""
API_Secret = ""
Access_Token = ""
Access_Token_Secret = ""
twitter_final = Twython(API_Key, API_Secret,
                  Access_Token, Access_Token_Secret)
influential_users = []
for (path,dir,file) in os.walk('path to directory') :
    influential_users.extend(dir)
    break
for i in range(0,2):
    print("---------------------------------------------------")
    print('Scraping followers profile of:', influential_users[i].split("_")[1])
    followers = pd.read_csv(path + "/" + influential_users[i] + '/followers.csv',sep=',')
    #followers = followers[0:3000]
    for index,row in followers.iterrows():
        id = row['id']
        name = str(row['name']).replace('/','_')
        user_name = row['screen_name']
        if not os.path.exists(path + '/' + influential_users[i] +  '/followers_timeline'):
            os.mkdir(path + '/' + influential_users[i] +  '/followers_timeline')
        print('***************************')
        print("Scraping user:",name)
        alltweets = []
        new_tweets = []
        if not os.path.isfile(path + '/' + influential_users[i] +  '/followers_timeline' + '/' + name + '.csv'):
            try:
                new_tweets = twitter_final.get_user_timeline(user_id = id,screen_name = user_name,count = 200,include_rts='true')
                alltweets.extend(new_tweets)
            except TwythonRateLimitError as error:
                remainder = float(twitter_final.get_lastfunction_header(header='X-Rate-Limit-Reset')) - time.time()
                del twitter_final
                if remainder > 0:
                    time.sleep(remainder)
                else:
                    remainder *= -1
                    time.sleep(remainder)
                twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                new_tweets = twitter_final.get_user_timeline(user_id = id,count=200,include_rts='true')
                alltweets.extend(new_tweets)
            except TwythonError as e:
                if e.error_code == 404:
                    followers = followers[followers.name != '.']
                    followers.to_csv(path + "/" +  influential_users[i] + '/followers.csv',index=False)
                    continue
                elif e.error_code == 429:
                    del twitter_final
                    time.sleep(900)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    new_tweets = twitter_final.get_user_timeline(user_id = id,count=200,include_rts='true')
                    alltweets.extend(new_tweets)
            total = len(alltweets)
            try:
                oldest = alltweets[-1]["id"] - 1
            except IndexError as e:
                with open(path + '/' + influential_users[i] +  '/followers_timeline' + '/' + name + '.csv',"w",newline='') as ap:
                    writer = csv.writer(ap)
                    writer.writerow(["id","created_at","text","original_user"])
                    writer.writerow([None,None,None,None])
                    ap.close()
                print('no statuses by this follower')
                continue
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(alltweets[-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            print ("...%s tweets downloaded so far" % (total))
        else:
            with open(path + '/' + influential_users[i] +  '/followers_timeline' + '/' + name + '.csv',"r") as re:
                rows = csv.reader(re,delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    new_tweets.append(row)
                re.close()
            total = len(new_tweets)
            if len(new_tweets) == 2:
                print('no statuses by this follower')
                continue
            elif len(new_tweets) < 3150:
                print('already scraped')
                continue
            else:
                oldest = int(new_tweets[-1][0]) - 1
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(new_tweets[-1][1],'%a %b %d %H:%M:%S +0000 %Y'))
            print ("...%s tweets downloaded so far" % (total))
        ts = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
        stop_date = datetime.strptime('2017-01-01','%Y-%m-%d')
        while ts.year >= stop_date.year and len(new_tweets) > 0:
                del new_tweets [:]
                print("getting tweets before %s" % (oldest))
                try:
                    new_tweets = twitter_final.get_user_timeline(user_id = id,count=200,max_id=oldest,include_rts='true')
                except TwythonRateLimitError as error:
                    remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    del twitter_final
                    if remainder > 0:
                        time.sleep(remainder)
                    else:
                        remainder *= -1
                        time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    new_tweets = twitter_final.get_user_timeline(user_id = id,count=200,max_id=oldest)
                except TwythonError as e:
                    if e.error_code == 404:
                        followers = followers[followers.name != '.']
                        followers.to_csv(path + "/" + influential_users[i] + '/followers.csv',index=False)
                        continue
                    elif e.error_code == 429:
                        del twitter_final
                        time.sleep(900)
                        twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                        new_tweets = twitter_final.get_user_timeline(user_id = id,count=200,include_rts='true')
                alltweets.extend(new_tweets)
                total += len(new_tweets)
                if len(new_tweets) != 0:
                    oldest = alltweets[-1]["id"] - 1
                    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(alltweets[-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
                    ts = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
                    print(len(new_tweets))
                    print ("...%s tweets downloaded so far" % (total))
                else:
                    print('no more tweets')
                    continue
        try:
            outtweets = [[tweet['id_str'], tweet['created_at'], tweet['text'].encode("utf-8"),tweet['retweeted_status']["user"]["screen_name"]]
                            for tweet in alltweets]
        except KeyError:
            outtweets = [[tweet['id_str'], tweet['created_at'], tweet['text'].encode("utf-8"),tweet["user"]["screen_name"]]
                            for tweet in alltweets]
        try:
            ap = open(path + '/' + influential_users[i] +  '/followers_timeline' + '/' + name + '.csv',"a",newline='')
            writer = csv.writer(ap)
            writer.writerows(outtweets)
            ap.close()
        except FileNotFoundError:
            with open(path + '/' + influential_users[i] +  '/followers_timeline' + '/' + name + '.csv',"w",newline='') as ap:
                writer = csv.writer(ap)
                writer.writerows(["id","created_at","text","original_user"])
                writer.writerows(outtweets)
                ap.close()
print('completed')
