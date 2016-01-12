from mysql import connector
from mysql.connector import errorcode
from getpass import getpass
from configmanager import PMConfig

print("This script will setup a database and a config file that will be used by the Ping Web Monitor.")
root_pw = getpass("Please enter the root password of the MySQL: ")
db_name = input("Please enter a name of the database: ")
user_name = input("Please enter the database user name: ")
user_pw = getpass("Please enter the database user password: ")

config = {
  'user': 'root',
  'password': root_pw,
  'host': '127.0.0.1',
  'database': 'mysql',
}

TABLES = {}

TABLES['1groups'] = (
    "CREATE TABLE `groups` ("
    "   `id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `name` char(30) NOT NULL,"
    "   PRIMARY KEY (`id`))")

TABLES['2servers'] = (
    "CREATE TABLE `servers` ("
    "   `server_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `name` varchar(30) NOT NULL,"
    "   `group_id` int(11) NOT NULL,"
    "   `address` varchar(45) NOT NULL,"
    "   PRIMARY KEY (`server_id`),"
    "   UNIQUE (`name`),"
    "   FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE)")

connection = connector.connect(**config)
cursor = connection.cursor()


def create_db():
    try:
        cursor.execute("CREATE DATABASE {} CHARACTER SET `utf8` COLLATE `utf8_general_ci`;".format(db_name))
    except connector.Error as err:
        print(err.msg)
        exit(1)
    else:
        print("\'pmon\' database created successfully!")

# Connecting to database
try:
    connection.database = db_name
except connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_db()
        connection.database = db_name
    else:
        print(err)
        exit(1)
# Create a user
try:
    print("Creating user {}: ".format(user_name), end='')
    cursor.execute("CREATE USER `{}`@`localhost` IDENTIFIED BY \'{}\'".format(user_name, user_pw))
except connector.Error as err:
    if err.errno == errorcode.ER_CANNOT_USER:
        print("already exists")
    else:
        print(err)
        exit(1)
else:
    print("OK")
# User rights mess
try:
    print("Granting privileges on {} to {}.".format(db_name,user_name))
    cursor.execute("GRANT ALL PRIVILEGES ON {}.* TO `{}`@`localhost`".format(db_name, user_name))
except connector.Error as err:
    print(err)
    exit(1)
# Create tables
for name, ddl in sorted(TABLES.items()):
    try:
        print("Creating table {}: ".format(name[1:]), end='')
        cursor.execute(ddl)
    except connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err)
            exit(1)
    else:
        print('OK')

cursor.close()
connection.close()

conf = PMConfig()
conf.set_db_config(db_name, user_name, user_pw)