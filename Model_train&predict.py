import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
train = pd.read_csv('train_data.csv',sep=',')
test = pd.read_csv('test_data.csv',sep=',')
cols = [col for col in train.columns if col != 'Bot']
X_train = train[cols]
cols = [col for col in train.columns if col not in ['Bot','description','screen_name','screen_name_length']]
X_train = train[cols]
y_train = train['Bot']
screen_names_train = train['screen_name']
X_test = test[cols]
y_test = test['Bot']
screen_names_test = test['screen_name']
#random forest classifier
RFC = RandomForestClassifier(50,'entropy')
RFC.fit(X_train,y_train)
print('Accuracy of random forest classifier on training set: {:.2f}'
     .format(RFC.score(X_train, y_train)))
print('Accuracy of random forest classifier on test set: {:.2f}'
     .format(RFC.score(X_test, y_test)))
# logistic regression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
print('Accuracy of Logistic regression classifier on training set: {:.2f}'
     .format(logreg.score(X_train, y_train)))
print('Accuracy of Logistic regression classifier on test set: {:.2f}'
     .format(logreg.score(X_test, y_test)))
# Descion tree
clf = DecisionTreeClassifier().fit(X_train, y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'
     .format(clf.score(X_train, y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'
     .format(clf.score(X_test, y_test)))
#KNN classifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(X_test, y_test)))
# LDA
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
print('Accuracy of LDA classifier on training set: {:.2f}'
     .format(lda.score(X_train, y_train)))
print('Accuracy of LDA classifier on test set: {:.2f}'
     .format(lda.score(X_test, y_test)))
# Gaussian Naive Bayes
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'
     .format(gnb.score(X_train, y_train)))
print('Accuracy of GNB classifier on test set: {:.2f}'
     .format(gnb.score(X_test, y_test)))
# Random forest regressor
rf = RandomForestRegressor(n_estimators = 1000, random_state = 50)
rf.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'
     .format(rf.score(X_train, y_train)))
print('Accuracy of GNB classifier on test set: {:.2f}'
     .format(rf.score(X_test, y_test)))
#Support Vector Machines
svm = SVC()
svm.fit(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'
     .format(svm.score(X_train, y_train)))
print('Accuracy of SVM classifier on test set: {:.2f}'
     .format(svm.score(X_test, y_test)))
