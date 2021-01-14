import mysql.connector
from datetime import date
import datetime

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "tata"
)

mycursor = db.cursor()

print(mycursor.execute("SHOW DATABASES"))
for x in mycursor:
    print(x)