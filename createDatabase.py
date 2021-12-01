import csv
import mysql.connector


# function creates the connection to mysql and returns the connection variable cnx
# and the cursor variable used access the database.
def connectToMySQL():
    cnx = mysql.connector.connect(password='project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


# function creates the menagerie database passed as the parameter DB_NAME
def createDatabase(cursor, DB_NAME):
    '''
    :param cursor: instance of the connection to the database
    :param DB_NAME: name of the database to create
    Creates the database at cursor with the given name.
    '''
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


# reads the data from a csv and inserts the data into a the tables
def insertDataWinter(cursor, input_file):
    with open(input_file) as f:
        # reads in the csv file using csv.reader()
        file_data = csv.reader(f)
        # skip the headers
        next(file_data)
        # sets for each table to remove duplicates
        game = set([])
        event = set([])
        athlete = set([])
        medalists = set([])

        # inserts the non duplicate values into each table set
        for row in file_data:
            game.add((row[0], row[1]))
            event.add((row[3], row[7], row[2]))
            athlete.add((row[4], row[5], row[6]))
            medalists.add((row[4], row[5], row[6], row[3], row[7], row[2], row[0], row[8]))

        # uses the table sets to create the insert queries
        for row in game:
            data = ''
            data += '' + row[0] + ',' + '"' + row[1] + '"'
            sql = "INSERT INTO Winter_Game VALUES (" + data + ");"
            cursor.execute(sql)

        # need and eventID because of two '1000M' events
        eventID = 1
        # so we can get he index of each event for the medal table
        events = []
        for row in event:
            data = ''
            data += '"' + str(eventID) + '", "' + row[0] + '",' + '"' + row[1] + '",' + '"' + row[2] + '"'
            sql = "INSERT INTO Winter_Event VALUES (" + data + ");"
            cursor.execute(sql)
            eventID += 1
            events.append(row)

        # need an athleteID because of the two 'RUZICKA, Vladimir' from different countries
        athleteID = 1
        # so we can get the index of each athlete for the medal table
        athletes = []
        for row in athlete:
            data = ''
            data += '"' + str(athleteID) + '", "' + row[0] + '",' + '"' + row[1] + '",' + '"' + row[2] + '"'
            sql = "INSERT INTO Winter_Athlete VALUES (" + data + ");"
            cursor.execute(sql)
            athleteID += 1
            athletes.append(row)

        # indexes the values need to determine the athleteID and eventID and adds one because indexes start at zero
        for row in medalists:
            data = ''
            data += '"' + str(athletes.index((row[0], row[1], row[2])) + 1) + '",' + '"' \
                    + str(events.index((row[3], row[4], row[5])) + 1) + '",' + '"' + row[6] + '", "' + row[7] + '"'
            sql = "INSERT INTO Winter_Medalists VALUES (" + data + ");"
            cursor.execute(sql)
    f.close()


# reads the data from a csv and inserts the data into a the tables
def insertDataSummer(cursor, input_file):
    with open(input_file) as f:
        # reads in the csv file using csv.reader()
        file_data = csv.reader(f)
        # skip the headers
        next(file_data)
        # sets for each table to remove duplicates
        game = set([])
        event = set([])
        athlete = set([])
        medalists = set([])

        # inserts the non duplicate values into each table set
        for row in file_data:
            game.add((row[0], row[1]))
            event.add((row[3], row[7], row[2]))
            athlete.add((row[4], row[5], row[6]))
            medalists.add((row[4], row[5], row[6], row[3], row[7], row[2], row[0], row[8]))

        # uses the table sets to create the insert queries
        for row in game:
            data = ''
            data += '' + row[0] + ',' + '"' + row[1] + '"'
            sql = "INSERT INTO Summer_Game VALUES (" + data + ");"
            cursor.execute(sql)

        # need and eventID because of two '1000M' events
        eventID = 1
        # so we can get he index of each event for the medal table
        events = []
        for row in event:
            data = ''
            data += '"' + str(eventID) + '", "' + row[0] + '",' + '"' + row[1] + '",' + '"' + row[2] + '"'
            sql = "INSERT INTO Summer_Event VALUES (" + data + ");"
            cursor.execute(sql)
            eventID += 1
            events.append(row)

        # need an athleteID because of the two 'RUZICKA, Vladimir' from different countries
        athleteID = 1
        # so we can get the index of each athlete for the medal table
        athletes = []
        for row in athlete:
            data = ''
            # Some names had nicknames (JEROME, Henry Winston "Harry") replaced the " to a ' so sql would work
            data += '"' + str(athleteID) + '", "' + row[0].replace('\"', "'") + '",' + '"' + row[1] + '",' + '"' + row[2] + '"'
            sql = "INSERT INTO Summer_Athlete VALUES (" + data + ");"
            cursor.execute(sql)
            athleteID += 1
            athletes.append(row)

        # indexes the values need to determine the athleteID and eventID and adds one because indexes start at zero
        for row in medalists:
            data = ''
            data += '"' + str(athletes.index((row[0], row[1], row[2])) + 1) + '",' + '"' \
                    + str(events.index((row[3], row[4], row[5])) + 1) + '",' + '"' + row[6] + '", "' + row[7] + '"'
            sql = "INSERT INTO Summer_Medalists VALUES (" + data + ");"
            cursor.execute(sql)
    f.close()


def main():
    DB_NAME = 'OlympicMedals'
    cursor, connection = connectToMySQL()
    cursor.execute('DROP DATABASE IF EXISTS ' + DB_NAME + ';')  # drops the database before it is created
    createDatabase(cursor, DB_NAME)  # Creates the database
    cursor.execute("USE {}".format(DB_NAME))

    # Reads the sql create tables statements and creates the tables
    with open('tables.sql', 'r') as f:
        for line in f:
            sql = line
            sql.strip() # remove the \n
            cursor.execute(sql)

    # inserts the data into the tables
    insertDataWinter(cursor, 'winter.csv')
    insertDataSummer(cursor, 'summer.csv')

    connection.commit()
    cursor.close()
    connection.close()


main()