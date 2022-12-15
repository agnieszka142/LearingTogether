#creatingdatabase
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="user",
  port=3306
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE elearningdatabase")
mycursor.execute("SHOW DATABASES")