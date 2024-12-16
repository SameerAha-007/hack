
import mysql.connector as db


mydb = db.connect(host = 'localhost', user = 'root', password = "Mahesh@123", db = 'hackathon')

cur = mydb.cursor()
cur.execute('insert into products values(1, "laptop",  "200", "flipcart")')
mydb.commit()
