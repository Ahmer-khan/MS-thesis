import pandas as pd
import os
import sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
train = pd.read_csv('train_data.csv',sep=',')
test = pd.read_csv('test_data.csv',sep=',')
train = train.append(test)
bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|yes_ofc|forget' \
                           r'expos|kill|clit|bbb|butt|fuck|XXX|sex|truthe|fake|anony|free|virus|funky|RNA|kuck|jargon' \
                           r'nerd|swag|jack|bang|bonsai|chick|prison|paper|pokem|xx|freak|ffd|dunia|clone|genie|bbb' \
                           r'ffd|onlyman|emoji|joke|troll|droop|free|every|wow|cheese|yeah|bio|magic|wizard|face'
words = []
for index,row in train.iterrows():
    if bag_of_words_bot in row["screen_name"]:
        words.append(1)
    else:
        words.append(0)
train["screen_name_contains_words"] = words
cols = [col for col in train.columns if col not in ['Bot','description','screen_name']]
X_train = train[cols]
y_train = train['Bot']
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
influential_user = []
for (path,dir,file) in os.walk(#path):
    influential_user.extend(dir)
    break
final_count = {}
for user in influential_user:
    print(user)
    tested = pd.read_csv(#path,sep=',')
    word_no = []
    for index,row in tested.iterrows():
        if bag_of_words_bot in row["screen_name"]:
            word_no.append(1)
        else:
            word_no.append(0)
    tested["screen_name_contains_words"] = word_no
    screen_names = tested['screen_name']
    tested = tested[cols]
    tested = tested.fillna(0)
    try:
        tested['BOT'] = lda.predict(tested)
    except:
        print('error')
        continue
    tested['screen_name'] = screen_names
    bots = tested[tested.BOT == 1]
    bots.to_csv(#path,index=False)
    try:
        name = user.split('_')[1]
    except:
        name = trend
    final_count[name] = {}
    final_count[name]['total followers'] = len(tested)
    final_count[name]['total Bots'] = len(bots)
    final_count[name]['%age']= (len(bots)/len(tested)) * 100
final = pd.DataFrame.from_dict(final_count,orient='index')
