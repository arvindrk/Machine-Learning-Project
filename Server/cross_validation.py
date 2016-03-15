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
mydata = pd.read_csv("/Users/arvindrk/Downloads/data40Ksklearn.csv")
y = mydata["downloads"]
X = mydata.ix[:,:-1]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.2, random_state=0)
kf = KFold(4, n_folds=2)
for train, test in kf:
	clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=None, random_state=0).fit(X_train, y_train)
	d = clf.score(X_test, y_test)
	if (d>max_d):
		max_d = d
