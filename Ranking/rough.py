import string
import MySQLdb;

db = MySQLdb.connect(user= 'root', passwd = 'suna', db = 'dataset', host = 'localhost')
cursor=db.cursor()
file1=open("dummy.txt","r")
file2=open("mysco.txt","r")
line1=file1.readline()
line1=file1.readline()
i=1
while(line1):
	print "line",i
	B = [x for x in line1.split(' ') if x.strip()]
	downloads=int(B[0])
	genre=int(B[1][4:])
	size=float(B[2][2:])
	price=float(B[3][2:])
	rating=float(B[4][2:])
	reviews=int(B[5][2:])
	name=B[7]
	line2=file2.readline()
	C = [t for t in line2.split('	') if t.strip()]
	score=float(C[2])
	print score
	cursor.execute("INSERT INTO scores values(%d,'%s',%d,%f,%f,%f,%d,'%s',%f);"%(i,name,genre,size,price,rating,reviews,downloads,score))
	db.commit()
	i=i+1
	line1=file1.readline()
db.close()