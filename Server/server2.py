from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
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

        print "Data Received from Browser\n"

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if (field == 'name'):
                self.name = form[field].value
            elif (field == 'rank'):
                self.rank = int(form[field].value)
            elif (field == 'genre'):
                self.genre = int(form[field].value)
            elif (field == 'downloads'):
                self.downloads = int(form[field].value)

        print "Please Wait, Data is Being Processed...\n"

        temp_genre = ''
        temp_downloads = ''
        temp_rank = ''
        if(self.genre != -1):
            temp_genre = 'genre = '+str(self.genre)
            if(self.downloads != -1):
                temp_downloads = ' AND downloads = '+str(self.downloads)
            elif(self.rank != -1):
                temp_rank = ' AND rank < '+str(self.rank)
        elif(self.downloads != -1):
            temp_downloads = 'downloads = '+str(self.downloads)
            if(self.rank != -1):
                temp_rank = ' AND rank < '+str(self.rank)
        elif(self.rank != -1):
            temp_rank = 'rank < '+str(self.rank)

        sql = "SELECT size,count(size) FROM ranked_games WHERE %s %s %s GROUP BY size ORDER BY count(size) DESC"%(temp_genre, temp_downloads, temp_rank)
        cursor.execute(sql)
        results = cursor.fetchall()
        size = float(results[0][0])
        self.wfile.write('%f;'%(size))

        sql = "SELECT rating,count(rating) FROM ranked_games WHERE %s %s %s GROUP BY rating ORDER BY count(rating) DESC"%(temp_genre, temp_downloads, temp_rank)
        cursor.execute(sql)
        results = cursor.fetchall()
        rating = float(results[0][0])
        self.wfile.write('%f;'%(rating))

        sql = "SELECT AVG(review_count) FROM ranked_games WHERE %s %s %s"%(temp_genre, temp_downloads, temp_rank)
        cursor.execute(sql)
        results = cursor.fetchall()
        rc = int(results[0][0])
        self.wfile.write('%d;'%(rc))

        sql = "SELECT genre,count(genre) FROM ranked_games WHERE %s %s %s GROUP BY genre ORDER BY count(genre) DESC"%(temp_genre, temp_downloads, temp_rank)
        cursor.execute(sql)
        results = cursor.fetchall()
        genre = int(results[0][0])
        self.wfile.write('%d;'%(genre))

        sql = "SELECT count(downloads) FROM ranked_games WHERE %s %s %s GROUP BY downloads ORDER BY count(downloads) DESC"%(temp_genre, temp_downloads, temp_rank)
        cursor.execute(sql)
        results = cursor.fetchall()
        i = 0
        length = len(results)
        while (i < length):
            self.wfile.write('%s'%(str(results[i])))
            if(i < length - 1):
                self.wfile.write('-')
            i = i + 1
        print "Data Process Completed!\nResponse Generated : \n" 
        print str(self.name)+" "+str(genre)+" "+str(size)+" "+str(rating)+" "+str(rc)+" "+str(results)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    
    server = HTTPServer(('localhost', 8001), PostHandler)
    print 'Starting Analysis Engine at 8001.\nEngine Listening...'
    server.serve_forever()