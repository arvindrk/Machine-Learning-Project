from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# max_a = 0
# max_b = 0
# max_c = 0
# max_d = 0

# for x in xrange(35000):
	# if(x>50):
		# threshold = x
		# print "Running ",x
mydata = pd.read_csv("/Users/arvindrk/Downloads/data40Ksklearn.csv")
y = mydata["downloads"]
X = mydata.ix[:,:-1]

# X_train, X_test = X[:37500], X[37500:]
# y_train, y_test = y[:37500], y[37500:]

X_train = X[:37500]
y_train = y[:37500]
a1,b1,c1,d1,e1 = 17, 125, 99, 1, 23299999

X_test = [a1,b1,c1,d1,e1]
# y_test = [f1]
clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
print clf.predict(X_test)
# a = clf.score(X_test, y_test)
# if (a>max_a):
# 	max_a = a
# 	thresh_a = threshold

clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
print clf.predict(X_test)
# b = clf.score(X_test, y_test)
# if (b>max_b):
# 	max_b = b
# 	thresh_b = threshold

clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
print clf.predict(X_test)
# c = clf.score(X_test, y_test)
# if (c>max_c):
# 	max_c = c
# 	thresh_c = threshold

clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=None, random_state=0).fit(X_train, y_train)
print clf.predict(X_test)
# d = clf.score(X_test, y_test)
# if (d>max_d):
# 	max_d = d
# 	thresh_d = threshold

		
# print "FINAL VALUES ->"		
# print "DecisionTreeClassifier max : ", a
# print "RandomForestClassifier max : ", b
# print "ExtraTreesClassifier max : ", c
# print "GradientBoostingClassifier max : ", d