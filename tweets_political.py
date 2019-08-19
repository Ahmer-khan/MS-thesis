import os
import shutil
if not os.path.exists('trends_tweets_dataset_political'):
    os.makedirs('trends_tweets_dataset_political')
for(dirpath,dirnames,filenames) in os.walk('trends_tweets_dataset'):
    for name in dirnames :
        new_dir = os.path.join(dirpath,name)
        file = os.listdir(new_dir)
        if file != []:
            file_path = os.path.join(new_dir,file[0])
            file_size = os.path.getsize(file_path)
            trend1 = name.split("_")
            del trend1[0]
            if file_size > 0:
                if "PML-N" in str(trend1[0]) or "PPP" in str(trend1[0]) or "PTI" in str(trend1[0]) or "Nawaz" in str(trend1)\
                    or "sharif" in str(trend1[0]) or "panama" in str(trend1[0]) or "Maryam" in str(trend1[0]) or\
                    "Bhutto" in str(trend1[0]) or "bilawal" in str(trend1[0]) or "IK" in str(trend1[0]) or "imran" in str(trend1[0])\
                        or "zardari" in str(trend1[0]):
                    if not os.path.exists('trends_tweets_dataset_political/' + trend1[0]):
                        os.makedirs('trends_tweets_dataset_political/' + trend1[0])
                        shutil.move(file_path,'trends_tweets_dataset_political/' + trend1[0])
