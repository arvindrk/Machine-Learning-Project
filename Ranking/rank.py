import string
import MySQLdb;

db = MySQLdb.connect(user= 'root', passwd = 'suna', db = 'dataset', host = 'localhost')
cursor=db.cursor()
x = 0
i = 1
for x in xrange(20):
	sql = "SELECT * FROM scores WHERE genre = %d ORDER BY score DESC;" % (x)
	# try:
	# Execute the SQL command
	cursor.execute(sql)
	# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	print x
	rank=0
	for row in results:
		sno = int(row[0])
		name = row[1]
		genre = int(row[2])
		size = float(row[3])
		price = float(row[4])
		rating = float(row[5])
		reviews = int(row[6])
		downloads = int(row[7])
		score = float(row[8])
		rank = rank +1 
		cursor2=db.cursor()
		cursor.execute("INSERT INTO ranked_games values(%d,%d,'%s',%d,%f,%f,%f,%d,'%s',%f);"%(i,rank,name,genre,size,price,rating,reviews,downloads,score))
		i = i + 1
		db.commit()
		# Now print fetched result
		print "SNO : ",i," Rank : ",rank," Genre : ",genre
	# except:
	#    print "Error: unable to fecth data"
db.close()
#INSERT INTO sorted(name,genre,size,price,rating,reviews,downloads,score)
#    SELECT name,genre,size,price,rating,reviews,downloads,score
#    FROM sam WHERE genre =2 ORDER BY `score` DESC