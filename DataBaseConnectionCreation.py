"""
Created on Thu Feb 12 2022

@author: Kawtar

"""

import mysql.connector as  mysql
from   mysql.connector import Error

# For Windows users: the default credentials in phpMyAdmin are user='root', password='', you can use another Mysql Server UI 
try:
    connection = mysql.connect(host='localhost', user='root',  # Establishing the connection with Mysql server
                        password='root')
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS LOL") #creating the database
        # print("Database is created")

except Error as e:
    print("Error while connecting to MySQL", e)

connection = mysql.connect(host='localhost', database='LOL',
    					 user='root', password='root') # Establishing the connection with MySql server and specific database 