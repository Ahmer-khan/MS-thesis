from twython import Twython, TwythonRateLimitError, TwythonError
import os,time
import pandas as pd
API_Key = ""
API_Secret = ""
Access_Token = ""
Access_Token_Secret = ""
twitter_final = Twython(API_Key, API_Secret,
                  Access_Token, Access_Token_Secret)
influential_user_list = pd.read_csv(#path)
influential_user_list = influential_user_list[0:5]
for index,row in influential_user_list.iterrows():
    row['name'] = row['name'].replace("b'","")
    row['name'] = row['name'].replace("'","")
    row['name'] = row['name'].replace(" ","")
    row['user_name'] = row['user_name'].replace("b'@","")
    row['user_name'] = row['user_name'].replace("'","")
    if not os.path.isfile(#path) :
        print("---------------------------------------------------")
        print('Scraping followers of:', row['name'],)
        next_cursor = -1
        followers_list = []
        while next_cursor != 0 :
            try:
                followers_element = twitter_final.get_followers_ids(screen_name = row['user_name'], cursor = next_cursor,count = 5000)
                followers_list.extend(followers_element['ids'])
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
        with open(#path) as f:
            for id in followers_list:
                print(id,file=f)
            f.close()
        print("---------------------------------------------------")
print('completed')
