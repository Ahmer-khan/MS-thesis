from twython import Twython, TwythonRateLimitError, TwythonError
import os
import time
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
for i in range(0,stop):
        trend = trends[i]
        print("---------------------------------------------------")
        print("Starting for trend : ", trend)
        try:
            users = open(path +"/" + trend + "/unique_retweeters.txt", "r")
            total_to_be_processed = len(users.readlines())
            print("Total Users : ", total_to_be_processed)
            users.close()
            users = open(path +"/" + trend + "/unique_retweeters.txt", "r")
            if not os.path.exists(path +"/" + trend + '/retweeters'):
                os.makedirs(path +"/" + trend + '/retweeters')
            users_list = []
            try:
                for (dirpath, dirnames, filenames) in os.walk(path +"/" + trend + '/retweeters'):
                    users_list.extend(dirnames)
                    break
                test = []
                for user in users_list:
                    test.append(int(user.split('_')[0]))
                highest = max(test)
            except:
                highest = 0
            print("Remaining users : " + str(total_to_be_processed - highest))
            username_list = users.readlines()
            for i in range(highest , total_to_be_processed):
                print("Processing User : ", i+1,
                      "/", total_to_be_processed)
                username = username_list[i].replace("\n","")
                try:
                     user_element = twitter_final.show_user(user_id= username)
                     if not os.path.exists(path +"/" + trend + '/retweeters/' + str(i) + "_" + user_element["screen_name"]):
                        os.makedirs(path +"/" + trend + '/retweeters/' + str(i) + "_" + user_element["screen_name"])
                     with open(path +"/" + trend + '/retweeters/' + str(i) + "_" + user_element["screen_name"] + '/user_profile_info.txt', 'w') as file:
                        file.write(json.dumps(user_element))
                        print("information for user: " + username + " gathered")
                     file.close()
                except TwythonRateLimitError as error:
                    remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                    del twitter_final
                    if remainder > 0:
                        time.sleep(remainder)
                    else:
                        remainder *= -1
                    time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                    i -= 1
                    continue
                except TwythonError as e:
                    if e.error_code == 403:
                        if not os.path.exists(path +"/" + trend + '/retweeters/' + str(i) + "_" + username):
                            os.makedirs(path +"/" + trend + '/retweeters/' + str(i) + "_" + username)
                        with open(path +"/" + trend + '/retweeters/' + str(i) + "_" + username + "/No_such_user.txt", 'w') as file:
                            file.close()
                        print("no such user")
                        continue
            users.close()
            print("---------------------------------------------------")
            print('')
        except:
            print("---------------------------------------------------")
            print('')
            continue
print("completed")
