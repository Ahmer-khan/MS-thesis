import pandas as pd
import os
influential_users = []
for (path,dir,files) in os.walk(#path):
    influential_users.extend(dir)
    break
final_dict = {}
for i in range(0,len(influential_users)):
    print('finding intersection of: ' + influential_users[i])
    try:
        bots = pd.read_csv(#path)
    except FileNotFoundError:
        continue
    original = pd.read_csv(#path)
    features = ['screen_name','created_at']
    original= original[features]
    for q in range (i+1,len(influential_users)):
        try:
            bots2 = pd.read_csv(#path)
        except FileNotFoundError:
            continue
        original1 = pd.read_csv(#path)
        original1 = original1[features]
        test1 = original.append(original1)
        selection1 = test1.duplicated(subset=['screen_name'],keep='first')
        test1 = test1[selection1]
        test = bots.append(bots2)
        selection = test.duplicated(subset=['screen_name'],keep='first')
        test = test[selection]
        test = test.merge(test1,how='inner',on=['screen_name'])
        test = test.sort_values('created_at')
        if not os.path.exists(path + '/common_bots'):
            os.mkdir(path + '/common_bots')
        name = influential_users[i].split('_')[1] + '&' + influential_users[q].split('_')[1]
        final_dict[name] = {}
        final_dict[name][influential_users[i].split('_')[1] + " bots"] = len(bots)
        final_dict[name][influential_users[q].split('_')[1] + " bots"] = len(bots2)
        final_dict[name]['common_bots'] = len(test)
        test.to_csv(path + '/common_bots/' + name + '.csv',index=False)
final = pd.DataFrame.from_dict(final_dict,orient='index')
final.to_csv(#path)
print('completed')
