from twython import Twython, TwythonRateLimitError, TwythonError
import pandas as pd
import os,time
API_Key = "graMtDf92vK3QhS34S8CCOlmH"
API_Secret = "HDt6GZfUhEulRHgGWb12STILVEjHIPafHOYd6qGO0cAIJgxK8D"
Access_Token = "746410136831299584-MxszeTHoKsdTpkM4ESnCHExHs0Lu4WX"
Access_Token_Secret = "DlzjrLrlNjjTSMci9DmzaLAHmxXL20xTYfxHDC6u26aTm"
twitter_final = Twython(API_Key, API_Secret,
                  Access_Token, Access_Token_Secret)
influential_user_list = pd.read_csv('influential_user_list.csv',sep=',')
influential_user_list = influential_user_list[0:5]
for index,row in influential_user_list.iterrows():
    row['name'] = row['name'].replace("b'","")
    row['name'] = row['name'].replace("'","")
    row['name'] = row['name'].replace(" ","")
    row['user_name'] = row['user_name'].replace("b'@","")
    row['user_name'] = row['user_name'].replace("'","")
    if not os.path.exists('influential_user_follower/'+ str(row['Rank']) + "_" + row['name']) :
        print("---------------------------------------------------")
        print('Scraping followers of:', row['name'],)
        next_cursor = -1
        followers_list = []
        while len(followers_list) != 30000 :
            try:
                followers_element = twitter_final.get_followers_list(screen_name = row['user_name'], cursor = next_cursor,count = 200,
                                                                  skip_status = 1)
                followers_list.extend(followers_element['users'])
                next_cursor = followers_element['next_cursor']
                print("followers scraped so far:",str(len(followers_list)))
            except TwythonRateLimitError as error:
                remainder = float(twitter_final.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
                del twitter_final
                if remainder > 0:
                    time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                else:
                    remainder *= -1
                    time.sleep(remainder)
                    twitter_final = Twython(API_Key, API_Secret,Access_Token, Access_Token_Secret)
                continue
        followers = pd.DataFrame.from_dict(followers_list)
        os.mkdir('influential_user_follower/'+ str(row['Rank']) + "_" + row['name'])
        followers.to_csv('influential_user_follower/'+ str(row['Rank']) + "_" + row['name'] + "/followers.csv")
        print("---------------------------------------------------")
print('completed')
