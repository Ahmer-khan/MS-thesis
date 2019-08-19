import os
import pandas as pd
import time
from datetime import datetime,date
import numpy as np
influential_users = []
for (path,dir,file) in os.walk(#path) :
    influential_users.extend(dir)
    break
for user in influential_users:
    if os.path.isfile(#path):
        continue
    print("---------------------------------------------------")
    print('working on followers of:', user.split("_")[1])
    follower = pd.read_csv(#path)
    follower = follower.replace(to_replace=['True','False'],value=[1,0])
    follower = follower.replace(to_replace=[True,False],value=[1,0])
    #follower[['default_profile','default_profile_image','verified']] = follower[['default_profile','default_profile_image','verified']].astype(int)
    follower = follower.fillna({'description':0})
    #follower = follower.dropna()
    #follower = follower.fillna(0)
    #follower = follower[np.isfinite(follower['created_at'])] 
    #follower["timestamp"] = pd.to_datetime(follower["created_at"])
    features_profile = ['id','screen_name','name', 'statuses_count', 'followers_count','friends_count', 'favourites_count', 'listed_count',
                       'default_profile', 'default_profile_image','verified','description','created_at']
    follower = follower[features_profile]
    follower = follower.dropna()
    follower["timestamp"] = pd.to_datetime(follower["created_at"])
    del follower['created_at']
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
    for index,row in follower.iterrows():
        print("starting for user:",str(i) + '/' + str(len(follower)))
        i += 1
        user_dict[row['id']] = {}
        user_dict[row['id']]['profile_activity'] = []
        user_dict[row['id']]['retweet_activity'] = []
        user_dict[row['id']]['tweet_activity'] = []
        user_dict[row['id']]['total_tweets_user'] = 0
        user_dict[row['id']]['total_retweets_user'] = 0
        last_activity = 0
        previous_retweet = 0
        previous_tweet = 0
        diff = datetime.today() - row['timestamp']
        days.append(diff.days)
        count = 0
        length = len(str(row['screen_name']))
        lengths.append(length)
        for character in str(row["screen_name"]):
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
        name = str(row['name']).replace('/','_')
        #name = name.replace('.','')
        try:
            temp = pd.read_csv(#path)
            temp['created_at'] = pd.to_datetime(temp['created_at'])
        except ValueError:
            temp = pd.read_csv(#path)
            temp = temp[['created_at','text']]
            temp['created_at'] = pd.to_datetime(temp['created_at'])
        except FileNotFoundError:
            continue
        if not temp.empty:
            for number,line in temp.iterrows():
                if last_activity == 0:
                    last_activity = line['created_at']
                else:
                    time_diff_activity = last_activity - line["created_at"]
                    last_activity = line["created_at"]
                    user_dict[row['id']]['profile_activity'].append(time_diff_activity.total_seconds())
                if "RT" in str(line["text"]):
                    user_dict[row['id']]['total_retweets_user'] += 1
                    if previous_retweet == 0:
                        previous_retweet = line['created_at']
                    else:
                        time_diff_retweets = previous_retweet - line['created_at']
                        previous_retweet = line['created_at']
                        user_dict[row['id']]['retweet_activity'].append(time_diff_retweets.total_seconds())
                else:
                    user_dict[row['id']]['total_tweets_user'] += 1
                    if previous_tweet == 0:
                        previous_tweet = line["created_at"]
                    else:
                        time_diff_tweets = previous_tweet - line["created_at"]
                        previous_tweet = line["created_at"]
                        user_dict[row['id']]['tweet_activity'].append(time_diff_tweets.total_seconds())
    follower['days_active'] = days
    del follower['timestamp']
    follower['Screen_name_length'] = lengths
    follower['digits_in_name'] = digits
    follower["description_length"] = lengths_des
    follower["contains_words"] = words
    final_dict = {}
    for key,value in user_dict.items():
        final_dict[key] = {}
        final_dict[key]["total_tweets"] = user_dict[key]['total_tweets_user']
        final_dict[key]["total_retweets"] = user_dict[key]['total_retweets_user']
        if user_dict[key]['profile_activity'] != []:
            final_dict[key]["avg_profile_activity(sec)"] = sum(user_dict[key]['profile_activity'])/len(user_dict[key]['profile_activity'])
            final_dict[key]['min_profile_activity(sec)'] = min(user_dict[key]['profile_activity'])
            final_dict[key]['max_profile_activity(sec)'] = max(user_dict[key]['profile_activity'])
        else:
            final_dict[key]["avg_profile_activity(sec)"] = 0
            final_dict[key]['min_profile_activity(sec)'] = 0
            final_dict[key]['max_profile_activity(sec)'] = 0
        if user_dict[key]['tweet_activity'] != []:
            final_dict[key]["avg_tweet_activity(sec)"] = sum(user_dict[key]['tweet_activity'])/len(user_dict[key]['tweet_activity'])
            final_dict[key]['min_tweet_activity(sec)'] = min(user_dict[key]['tweet_activity'])
            final_dict[key]['max_tweet_activity(sec)'] = max(user_dict[key]['tweet_activity'])
        else:
            final_dict[key]["avg_tweet_activity(sec)"] = 0
            final_dict[key]['min_tweet_activity(sec)'] = 0
            final_dict[key]['max_tweet_activity(sec)'] = 0
        if user_dict[key]['retweet_activity'] != []:
            final_dict[key]["avg_retweet_activity(sec)"] = sum(user_dict[key]['retweet_activity'])/len(user_dict[key]['retweet_activity'])
            final_dict[key]['min_retweet_activity(sec)'] = min(user_dict[key]['retweet_activity'])
            final_dict[key]['max_retweet_activity(sec)'] = max(user_dict[key]['retweet_activity'])
        else:
            final_dict[key]["avg_retweet_activity(sec)"] = 0
            final_dict[key]['min_retweet_activity(sec)'] = 0
            final_dict[key]['min_retweet_activity(sec)'] = 0
    tweet_dataframe = pd.DataFrame(final_dict)
    tweet_dataframe = tweet_dataframe.transpose()
    tweet_dataframe.index.name = 'id'
    follower = follower.merge(tweet_dataframe,how='outer',left_on='id',right_index=True)
    follower.to_csv(#path)
print('completed')
