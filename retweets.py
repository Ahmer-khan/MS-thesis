from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import ast
from selenium.common.exceptions import TimeoutException
#browser = webdriver.Firefox()
chrome_options = webdriver.ChromeOptions()
executable_path = 'chromedriver.exe'
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
browser.set_window_size(1366, 768)
browser_link = 'https://twitter.com/login'
user = "ahmer.mathlete@gmail.com"
pwd = "cos30sin60"
browser.get(browser_link)
#assert "Login on Twitter" in browser.title
elem = browser.find_element_by_class_name("js-username-field")
elem.send_keys(user)
browser.implicitly_wait(3)
elem = browser.find_element_by_class_name("js-password-field")
elem.send_keys(pwd)
browser.implicitly_wait(5)
browser.find_element_by_class_name("EdgeButtom--medium").click()
browser.implicitly_wait(5)
for(path,dir,files) in os.walk("trends_tweets_dataset_political_test"):
    for name in dir:
        print(name)
        new_dir = os.path.join(path, name)
        file = os.listdir(new_dir)
        print(file)
        tweets = open(new_dir + "/" + file[1],"r")
        j = 0
        for line in tweets:
            line_dict = ast.literal_eval(line)
            retweets = open(new_dir + "/retweets.txt","r")
            for key in line_dict.keys():
                if int(line_dict[key]["retweets"]) > 0 :
                    #file_path = os.path.join(new_dir, file[0])
                    #file_size = os.path.getsize(file_path)
                    line_retweets_list = retweets.readlines()
                    if len(line_retweets_list) > 0 :
                        line_retweets_dict = ast.literal_eval(line_retweets_list[j])
                        keys = line_retweets_dict[key].keys()
                        if len(keys)!= int(line_dict[key]["retweets"]):
                            browser.get("https://twitter.com/" + line_dict[key]["user"] + "/status/" + key)
                            browser.implicitly_wait(5)
                            browser.find_element_by_class_name("request-retweeted-popup").click()
                            browser.implicitly_wait(6)
                            retweets.close()
                            try:

                                timeline = browser.find_element_by_xpath(
                                    '//*[@id="activity-popup-dialog-body"]/div[4]/ol')
                                tweets_online = timeline.find_elements_by_css_selector(
                                    'li.js-stream-item.stream-item.stream-item')
                                f = open(new_dir + "/retweets.txt","w")
                                for tweet in tweets_online:
                                    i = 1
                                    final = {}
                                    final[key] = {}
                                    final[key]["retweet user " + str(i)] = []
                                    top_info = tweet.find_element_by_css_selector(
                                        'div.stream-item-header')
                                    full_name = top_info.find_element_by_css_selector(
                                        'strong.fullname').text
                                    final[key]["retweet user " + str(i)].append(full_name)
                                    username = top_info.find_element_by_css_selector(
                                        'span.username.u-dir.u-textTruncate').text
                                    final[key]["retweet user " + str(i)].append(username)
                                    profile = top_info.find_element_by_css_selector('a.account-group.js-user-profile-link').get_attribute(
                                        'href')
                                    final[key]["retweet user " + str(i)].append(profile)
                                    print(final)
                                    print(str(i) + " retweets done")
                                    i += 1
                                    print(final,file=f)
                                print("all retweets for",key,"done")
                                f.close()
                                j += 1
                            except Exception as e :
                                 print(e)
                        else:
                            print("this tweet id : " + str(key) + " already done")
                    else:
                        print("no retweets gathered yet for this trend")
                        browser.get("https://twitter.com/" + line_dict[key]["user"] + "/status/" + key)
                        browser.implicitly_wait(5)
                        browser.find_element_by_class_name("request-retweeted-popup").click()
                        browser.implicitly_wait(6)
                        retweets.close()
                        try:
                            timeline = browser.find_element_by_xpath(
                                '//*[@id="activity-popup-dialog-body"]/div[4]/ol')
                            tweets_online = timeline.find_elements_by_css_selector(
                                'li.js-stream-item.stream-item.stream-item')
                            f = open(new_dir + "/retweets.txt","w")
                            for tweet in tweets_online:
                                i = 1
                                final = {}
                                final[key] = {}
                                final[key]["retweet user " + str(i)] = []
                                top_info = tweet.find_element_by_css_selector(
                                    'div.stream-item-header')
                                full_name = top_info.find_element_by_css_selector(
                                    'strong.fullname').text
                                final[key]["retweet user " + str(i)].append(full_name)
                                username = top_info.find_element_by_css_selector(
                                    'span.username.u-dir.u-textTruncate').text
                                final[key]["retweet user " + str(i)].append(username)
                                profile = top_info.find_element_by_css_selector('a.account-group.js-user-profile-link').get_attribute(
                                    'href')
                                final[key]["retweet user " + str(i)].append(profile)
                                print(final)
                                print(str(i) + " retweets done")
                                i += 1
                                print(final,file=f)
                            print("all retweets for",key,"done")
                            f.close()
                            j += 1
                        except Exception as e :
                            print(e)
                        else:
                            print(name,"already done")
                else:
                    print("no retweets on this tweet")
                #browser.close()
        tweets.close()
browser.quit()
print("end")
