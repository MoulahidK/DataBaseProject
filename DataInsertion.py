
"""
Created on Thu Feb 12 2022

@author: Kawtar
"""
import DataImport, DataBaseConnectionCreation
from   DataBaseConnectionCreation import Error, mysql, connection
from   DataImport import emported_data, winners_emported_data
try:
      # Checking if the connection is well established 
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Checking if the tables exist
        cursor.execute('DROP TABLE IF EXISTS `Match`;')
        cursor.execute('DROP TABLE IF EXISTS `Winners`;')
        print('Creating tables....')

		# Creating the tables using an SQL statement
        cursor.execute("CREATE TABLE  `LOL`.`Match` (`_id` varchar(15), `temps` int(2), `blue_ward_placed` int(1), `blue_ward_kill` int(1), `blue_level_up` int(1), `blue_champion_kill` int(1), `blue_champion_assist` int(2), `blue_champion_special_kill` int(1), `blue_elite_monster_kill` int(1), `blue_building_kill` int(1), `blue_turret_plate_destroyed` int(1), `blue_gold_earned` int(4), `blue_minions_killed` int(2), `red_ward_placed` int(1), `red_ward_kill` int(1), `red_level_up` int(1), `red_champion_kill` int(1), `red_champion_assist` int(2), `red_champion_special_kill` int(1), `red_elite_monster_kill` int(1), `red_building_kill` int(1), `red_turret_plate_destroyed` int(1), `red_gold_earned` int(4), `red_minions_killed` int(2)) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cursor.execute("CREATE TABLE  `LOL`.`Winners`( `_id` varchar(15), `team` varchar(15)) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")
        print("Tables are created....")

        # Loop through the Dataframe of the General Data
        for i,row in emported_data.iterrows(): # Inserting each Dataframe row to the table row
            sql = "INSERT INTO `LOL`.`Match` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,tuple(row))
        	#The connection is not auto committed by default, so we must commit to save our change
            connection.commit()
            print("General Record inserted")

        # Loop through the Dataframe of the Winners Data
        for i,row in winners_emported_data.iterrows(): # Inserting each Dataframe row to the table row
            sql = "INSERT INTO `LOL`.`Winners` VALUES (%s, %s)"
            cursor.execute(sql,tuple(row))
        	#The connection is not auto committed by default, so we must commit to save our change
            connection.commit()
            print("Winners Record inserted")
        print("DONE")

except Error as e:
            print("Error while connecting to MySQL", e)

