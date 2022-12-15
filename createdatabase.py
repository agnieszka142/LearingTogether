# importing required library
import mysql.connector

#creatingdatabase
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="user",
  port=3306
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS elearningdatabase")


# connecting to the database
dataBase = mysql.connector.connect(
					host = "localhost",
					user = "root",
					passwd = "user",
					database = "elearningdatabase",
                    port =3306)

# preparing a cursor object
cursorObject = dataBase.cursor()
# creating table
User = """CREATE TABLE IF NOT EXISTS User (
    ID_USER INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    UNIQUE (email,username)
)"""
UserPayment = """CREATE TABLE IF NOT EXISTS UserPayment (
    ID_PAYMENT INT PRIMARY KEY,
    ID_USER INT,
    name_of_payment VARCHAR(255),
    date DATE,
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER)
)"""
Administrator = """ CREATE TABLE IF NOT EXISTS Administrator (
    ID_USER INT PRIMARY KEY,
    rights ENUM('moderator', 'administrator'),
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER)
)"""
UserProfile = """ CREATE TABLE IF NOT EXISTS UserProfile (
    ID_USER INT PRIMARY KEY,
    picture BLOB,
    description VARCHAR(255),
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER)
)"""
FavCategories = """ CREATE TABLE IF NOT EXISTS FavCategories (
    ID_USER INT,
    ID_CATEGORY INT,
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER),
    FOREIGN KEY (ID_CATEGORY) REFERENCES Categories(ID_CATEGORY)
)"""
Categories = """ CREATE TABLE IF NOT EXISTS Categories (
    ID_CATEGORY INT PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255)
) """
CourseEnrolled = """ CREATE TABLE IF NOT EXISTS CourseEnrolled (
    ID_COURSE INT,
    ID_USER INT,
    FOREIGN KEY (ID_COURSE) REFERENCES Course(ID_COURSE),
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER)
)"""
CourseGrade = """ CREATE TABLE IF NOT EXISTS CourseGrade (
    ID_GRADE INT PRIMARY KEY,
    ID_USER INT,
    ID_COURSE INT,
    rate TINYINT CHECK (rate >= 1 AND rate <= 10),
    comment VARCHAR(255),
    FOREIGN KEY (ID_USER) REFERENCES User(ID_USER),
    FOREIGN KEY (ID_COURSE) REFERENCES Course(ID_COURSE)
)"""
TUMaterials = """ CREATE TABLE IF NOT EXISTS TUMaterials (
ID_MATERIAL INT PRIMARY KEY,
ID_TEACHINGUNIT INT,
material VARCHAR(255),
explanation VARCHAR(255),
FOREIGN KEY (ID_TEACHINGUNIT) REFERENCES TeachingUnits(ID_TEACHINGUNIT)
)"""

TeachingUnits = """ CREATE TABLE IF NOT EXISTS TeachingUnits (
ID_TEACHINGUNIT INT PRIMARY KEY,
ID_COURSE INT,
NAME VARCHAR(255),
DESCRIPTION VARCHAR(255),
CREDITS INT,
FOREIGN KEY (ID_COURSE) REFERENCES Course(ID_COURSE)
)"""

Course = """ CREATE TABLE IF NOT EXISTS Course (
ID_COURSE INT PRIMARY KEY,
ID_CATEGORY INT,
NAME VARCHAR(255),
DESCRIPTION TEXT,
LOGO VARCHAR(255),
PRICE DECIMAL(10,2),
DURATION INT,
FOREIGN KEY (ID_CATEGORY) REFERENCES Categories (ID_CATEGORY)
)"""
OnlineChat = """ CREATE TABLE IF NOT EXISTS OnlineChat (
ID_ONCH INT PRIMARY KEY,
ID_COURSE INT,
date DATE,
link VARCHAR(255),
registerednumber INT,
FOREIGN KEY (ID_COURSE) REFERENCES Course(ID_COURSE)
)"""

CourseOwners = """ CREATE TABLE IF NOT EXISTS CourseOwners (
ID_COURSE INT,
ID_USER INT,
permission ENUM('moderator', 'owner'),
FOREIGN KEY (ID_COURSE) REFERENCES Course(ID_COURSE),
FOREIGN KEY (ID_USER) REFERENCES User(ID_USER)
)"""
# table created #3 main tables
cursorObject.execute(User)
cursorObject.execute(Categories)
cursorObject.execute(Course)

#subtables
cursorObject.execute(UserPayment)
cursorObject.execute(UserProfile)
cursorObject.execute(Administrator)

cursorObject.execute(FavCategories)
cursorObject.execute(CourseEnrolled)
cursorObject.execute(CourseGrade)

cursorObject.execute(CourseOwners)
cursorObject.execute(OnlineChat)
cursorObject.execute(TeachingUnits)
cursorObject.execute(TUMaterials)



# disconnecting from server
dataBase.close()
