from sklearn.ensemble import GradientBoostingClassifier
from BaseHTTPServer import BaseHTTPRequestHandler
import pandas as pd
import time
import cgi
import subprocess
import MySQLdb

class PostHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Parse the form data poste
        db = MySQLdb.connect(user= 'root', passwd = 'suna', db = 'dataset', host = 'localhost')
        cursor=db.cursor()
        form = cgi.FieldStorage(
            fp=self.rfile,  
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        mydata = pd.read_csv("/Users/arvindrk/Downloads/data40Ksklearn.csv")
        y = mydata["downloads"]
        X = mydata.ix[:,:-1]
        X_train = X[:37500]
        y_train = y[:37500]
        self.size = 1
        print "Data Received from Browser\n"

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if (field == 'name'):
                self.name = form[field].value
            elif (field == 'price'):
                self.price = float(form[field].value)
            elif (field == 'size'):
                self.size = self.size * float(form[field].value)
            elif (field == 'sizeType'):
                self.sizeType = form[field].value
                if (self.sizeType == 'gb'):
                    self.size = self.size * 1000
            elif (field == 'rating'):
                self.rating = float(form[field].value)
            elif (field == 'genre'):
                self.genre = int(form[field].value)
            elif (field == 'review_count'):
                self.review_count = int(form[field].value)

        print "Please Wait, Data is Being Processed...\n"
        
        X_test = [self.genre, self.size, self.price, self.rating, self.review_count]
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=None, random_state=0).fit(X_train, y_train)
        # n_estimators = number of boosting stages to perform
        # max_depth = The maximum depth limits the number of nodes in the tree. Tune this parameter for best performance
        # .fit = Fit the gradient boosting model.

        temp =  clf.predict(X_test)
        y_test = temp;
        print clf.score(X_test,y_test)
        temp = int(temp[0])
        if temp == 0:
            downloads = " < 100,000"
        elif temp == 1:
            downloads = "100,000 - 1,000,000"
        elif temp == 2:
            downloads = "1,000,000 - 10,000,000"
        elif temp == 3:
            downloads = "10,000,000 - 100,000,000"
        elif temp == 4:
            downloads = "100,000,000 - 1,000,000,000"
        
        self.wfile.write('%s;'%(downloads))
        print "Data Process Completed!"        
        
        f = open('test.txt','w')
        string = str(temp)+" qid:"+str(self.genre)+" 1:"+str(self.size)+" 2:"+str(self.price)+" 3:"+str(self.rating)+" 4:"+str(self.review_count)+" # "+str(self.name)
        f.write(string)
        f.close()

        subprocess.call(['java', '-jar', '/Users/arvindrk/project/Ranking/RankLib-2.1-patched.jar', '-load', '/Users/arvindrk/project/Ranking/mymodel.txt', '-rank', '/Users/arvindrk/project/Server/test.txt', '-score', '/Users/arvindrk/project/Server/score.txt','-metric2T', 'ERR@10'])

        f = open('score.txt','r')
        line = f.readline()
        score = float(line[4:])
        print score

        sql = "SELECT * FROM ranked_games WHERE score <= %f AND genre = %d"%(score,self.genre)
        cursor.execute(sql)
        results = cursor.fetchall()
        db.commit()
        rank = int(results[0][1])
        print "Estimated Rank : ",rank
        self.wfile.write('%d'%(rank))
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    
    server = HTTPServer(('localhost', 8000), PostHandler)
    print 'Starting server at 8000, use <Ctrl-C> to stop'
    server.serve_forever()