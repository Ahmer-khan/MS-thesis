import os
import pandas as pd
import time
import ast
import json
from datetime import datetime,date
trends = []
for (path,dir,file) in os.walk('top_30') :
    trends.extend(dir)
    break
for trend in trends:
    last_final = pd.DataFrame()
    if os.path.isfile(path + '/' + trend + '/retweeters_final.csv'):
        continue
    print("---------------------------------------------------")
    print('working on retweeters of:', trend)
    retweeters = []
    for(add,fol,files) in os.walk(path + '/' + trend + '/retweeters'):
        retweeters.extend(fol)
        break
    i = 1
    retweeters_list = []
    for retweeter in retweeters:
        print("*******************************************")
        print('processing retweeter: ' + str(i) + '/' + str(len(retweeters)))
        print(retweeter)
        i += 1
        if os.path.isfile(add + '/' + retweeter + '/final.csv'):
            ser = pd.Series.from_csv(add + '/' + retweeter + '/final.csv',sep=',')
            frame = ser.to_frame()
            frame = frame.transpose()
            last_final = last_final.append(frame)
            continue
        final_dict = {}
        try:
            with open(add + '/' + retweeter + '/user_profile_info.txt','r') as f:
                for line in f:
                    line = line.replace('\n','')
                    line = line.replace('"','')
                    line = line.replace("{" , "")
                    line = line.replace("}" , "")
                    line = line.replace(" ", "")
                    temp = line.split(',')
                    for item in temp:
                        index = item.find(":")
                        final_dict[item[0:index]] = item[index+1:]
                final_dict['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(final_dict['created_at'],'%a%b%d%H:%M:%S+0000%Y'))
        except FileNotFoundError:
            continue
        user_dict = {}
        user_dict[final_dict['id']] = {}
        user_dict[final_dict['id']]['profile_activity'] = []
        user_dict[final_dict['id']]['retweet_activity'] = []
        user_dict[final_dict['id']]['tweet_activity'] = []
        user_dict[final_dict['id']]['total_tweets_user'] = 0
        user_dict[final_dict['id']]['total_retweets_user'] = 0
        last_activity = 0
        previous_retweet = 0
        previous_tweet = 0
        try:
            temp = pd.read_csv(add + '/' + retweeter + '/user_timeline.csv',sep=',',usecols=['text','created_at'],engine='python')
            temp['created_at'] = pd.to_datetime(temp['created_at'])
        except ValueError:
            temp = pd.read_csv(add + '/' + retweeter + '/user_timeline.csv',sep=',',header=None,names=['id','created_at','text','original_user'],engine='python')
            temp = temp[['created_at','text']]
            temp['created_at'] = pd.to_datetime(temp['created_at'])
        except FileNotFoundError:
            continue
        except:
            try:
                temp = pd.read_csv(add + '/' + retweeter + '/user_timeline.csv',sep=',',engine='python')
                temp = temp.rename(columns={ temp.columns[1]: "created_at",temp.columns[2]:"text" })
                temp = temp[:,1:3]
                temp['created_at'] = pd.to_datetime(temp['created_at'])
            except:
                print('error')
                continue
        if not temp.empty:
            for number,line in temp.iterrows():
                if last_activity == 0:
                    last_activity = line['created_at']
                else:
                    time_diff_activity = last_activity - line["created_at"]
                    last_activity = line["created_at"]
                    user_dict[final_dict['id']]['profile_activity'].append(time_diff_activity.total_seconds())
                if "RT" in str(line["text"]):
                    user_dict[final_dict['id']]['total_retweets_user'] += 1
                    if previous_retweet == 0:
                        previous_retweet = line['created_at']
                    else:
                        time_diff_retweets = previous_retweet - line['created_at']
                        previous_retweet = line['created_at']
                        user_dict[final_dict['id']]['retweet_activity'].append(time_diff_retweets.total_seconds())
                else:
                    user_dict[final_dict['id']]['total_tweets_user'] += 1
                    if previous_tweet == 0:
                        previous_tweet = line["created_at"]
                    else:
                        time_diff_tweets = previous_tweet - line["created_at"]
                        previous_tweet = line["created_at"]
                        user_dict[final_dict['id']]['tweet_activity'].append(time_diff_tweets.total_seconds())
        for key,value in user_dict.items():
            final_dict["total_tweets"] = user_dict[key]['total_tweets_user']
            final_dict["total_retweets"] = user_dict[key]['total_retweets_user']
            if user_dict[key]['profile_activity'] != []:
                final_dict["avg_profile_activity(sec)"] = sum(user_dict[key]['profile_activity'])/len(user_dict[key]['profile_activity'])
                final_dict['min_profile_activity(sec)'] = min(user_dict[key]['profile_activity'])
                final_dict['max_profile_activity(sec)'] = max(user_dict[key]['profile_activity'])
            else:
                final_dict["avg_profile_activity(sec)"] = 0
                final_dict['min_profile_activity(sec)'] = 0
                final_dict['max_profile_activity(sec)'] = 0
            if user_dict[key]['tweet_activity'] != []:
                final_dict["avg_tweet_activity(sec)"] = sum(user_dict[key]['tweet_activity'])/len(user_dict[key]['tweet_activity'])
                final_dict['min_tweet_activity(sec)'] = min(user_dict[key]['tweet_activity'])
                final_dict['max_tweet_activity(sec)'] = max(user_dict[key]['tweet_activity'])
            else:
                final_dict["avg_tweet_activity(sec)"] = 0
                final_dict['min_tweet_activity(sec)'] = 0
                final_dict['max_tweet_activity(sec)'] = 0
            if user_dict[key]['retweet_activity'] != []:
                final_dict["avg_retweet_activity(sec)"] = sum(user_dict[key]['retweet_activity'])/len(user_dict[key]['retweet_activity'])
                final_dict['min_retweet_activity(sec)'] = min(user_dict[key]['retweet_activity'])
                final_dict['max_retweet_activity(sec)'] = max(user_dict[key]['retweet_activity'])
            else:
                final_dict["avg_retweet_activity(sec)"] = 0
                final_dict['min_retweet_activity(sec)'] = 0
                final_dict['min_retweet_activity(sec)'] = 0
        retweeter_dataframe = pd.Series(final_dict)
        retweeter_dataframe.to_csv(add + '/' + retweeter + '/final.csv')
        retweeters_list.append(final_dict)
    last = pd.DataFrame.from_dict(retweeters_list)
    last_final = last_final.append(last)
    last_final = last_final.replace(to_replace=['True','False'],value=[1,0])
    last_final = last_final.replace(to_replace=['true','false'],value=[1,0])
    last_final = last_final.replace(to_replace=[True,False],value=[1,0])
    last_final = last_final.fillna(0)
    #last["timestamp"] = pd.to_datetime(last["created_at"])
    features_profile = ['id','screen_name','name', 'statuses_count', 'followers_count','friends_count', 'favourites_count', 'listed_count',
                       'default_profile', 'default_profile_image','verified','description','timestamp','avg_profile_activity(sec)','avg_retweet_activity(sec)',
                       'avg_tweet_activity(sec)','max_profile_activity(sec)','max_retweet_activity(sec)','max_tweet_activity(sec)','min_profile_activity(sec)',
                       'min_retweet_activity(sec)','min_tweet_activity(sec)','total_retweets','total_tweets',]
    last_final = last_final[features_profile]
    bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|yes_ofc|forget' \
                           r'expos|kill|clit|bbb|butt|fuck|XXX|sex|truthe|fake|anony|free|virus|funky|RNA|kuck|jargon' \
                           r'nerd|swag|jack|bang|bonsai|chick|prison|paper|pokem|xx|freak|ffd|dunia|clone|genie|bbb' \
                           r'ffd|onlyman|emoji|joke|troll|droop|free|every|wow|cheese|yeah|bio|magic|wizard|face'
    user_dict = {}
    i = 1
    days = []
    lengths = []
    digits = []
    lengths_des = []
    words = []
    for index,row in last_final.iterrows():
        diff = datetime.today() - datetime.strptime(row['timestamp'],'%Y-%m-%d %H:%M:%S')
        days.append(diff.days)
        count = 0
        length = len(row['screen_name'])
        lengths.append(length)
        for character in row["screen_name"]:
            try:
                int(character)
                count += 1
            except:
                continue
        digits.append(count)
        if row["description"] != 0:
            length = len(row["description"])
            if bag_of_words_bot in row["description"]:
                words.append(1)
            else:
                words.append(0)
        else:
            length = 0
            words.append(0)
        lengths_des.append(length)
    last_final['days_active'] = days
    del last_final['timestamp']
    last_final['Screen_name_length'] = lengths
    last_final['digits_in_name'] = digits
    last_final["description_length"] = lengths_des
    last_final["contains_words"] = words
    last_final.to_csv(path + '/' + trend + '/retweeters_final.csv',index=False)
print("completed")