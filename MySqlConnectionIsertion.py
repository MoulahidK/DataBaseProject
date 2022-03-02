
"""
Created on Thu Feb 12 2022

@author: Kawtar
"""

import pandas as pd

emported_data = pd.read_csv('/Users/macbookpro/Desktop/ExportCSV.csv', index_col=False, delimiter = ',')
# emported_data.head(5)

import mysql.connector as mysql
from mysql.connector import Error

# For Windows users: the default credentials in phpMyAdmin are user='root', password=''
try:
    connecion = mysql.connect(host='localhost', user='root',  # Establishing the connection with Mysql server
                        password='root')
    if connecion.is_connected():
        cursor = connecion.cursor()
        cursor.execute("CREATE DATABASE HR") #creating the database
        print("Database is created")

except Error as e:
    print("Error while connecting to MySQL", e)

try:
    connecion = mysql.connect(host='localhost', database='HR',
    					 user='root', password='root') # Establishing the connection with MySql server and specific database 
    if connecion.is_connected():
        cursor = connecion.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS person;')
        print('Creating table....')
		# Creating the table using an SQL statement
        cursor.execute("CREATE TABLE person(ID int(10), Job_title varchar(255), email_address varchar(255), firstLast_Name varchar(255))")
        print("Table is created....")
        # Loop through the Dataframe
        for i,row in emported_data.iterrows(): # Inserting each Dataframe row to the table row
            sql = "INSERT INTO HR.person VALUES (%i, %s, %s, %s)"
            cursor.execute(sql, tuple(row))
            # The connection is not auto committed by default, so we must commit to save our changes
            connecion.commit()
        print("Record inserted")
except Error as e:
            print("Error while connecting to MySQL", e)

