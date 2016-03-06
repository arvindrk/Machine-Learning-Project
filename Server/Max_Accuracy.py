from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

max_a = 0
max_b = 0
max_c = 0
max_d = 0

for x in xrange(35000):
	if(x>50):
		threshold = x
		print "Running ",x
		mydata = pd.read_csv("/Users/arvindrk/Downloads/data40Ksklearn.csv")
		y = mydata["downloads"]
		X = mydata.ix[:,:-1]
		X_train, X_test = X[:threshold], X[threshold:]
		y_train, y_test = y[:threshold], y[threshold:]

		clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
		a = clf.score(X_test, y_test)
		if (a>max_a):
			max_a = a
			thresh_a = threshold
		
		clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
		b = clf.score(X_test, y_test)
		if (b>max_b):
			max_b = b
			thresh_b = threshold
		
		clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0).fit(X_train, y_train)
		c = clf.score(X_test, y_test)
		if (c>max_c):
			max_c = c
			thresh_c = threshold
		
		clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=None, random_state=0).fit(X_train, y_train)
		d = clf.score(X_test, y_test)
		if (d>max_d):
			max_d = d
			thresh_d = threshold
		
print "FINAL VALUES ->"		
print "DecisionTreeClassifier max : ", max_a, "for threshold : ", thresh_a	
print "RandomForestClassifier max : ", max_b, "for threshold : ", thresh_b
print "ExtraTreesClassifier max : ", max_c, "for threshold : ", thresh_c
print "GradientBoostingClassifier max : ", max_d, "for threshold : ", thresh_d		