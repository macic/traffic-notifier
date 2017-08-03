from peewee import MySQLDatabase, Database
DB_LINK = 'mysql://root:magpies666@94.246.168.27:3306'
db = MySQLDatabase(DB_LINK)
print (db.execute_sql("SHOW DATABASES;"))
db.close()