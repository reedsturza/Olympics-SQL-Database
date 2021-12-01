import mysql.connector
from beautifultable import BeautifulTable


# function creates the connection to mysql and returns the connection variable cnx
# and the cursor variable used access the database.
def connectToMySQL():
    cnx = mysql.connector.connect(password='project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


# create a dictionary name queries that has the question letter as the key and stores
# the question and the query associated with that key as a list of 2 strings
def createQueries():
    queries = {}
    questionsFile = open("questions.txt", "r")
    queryFile = open("queries.sql", "r")
    for question in questionsFile:
        question = question.strip()
        query = queryFile.readline()
        query = query.strip()
        data = question.split(',')
        queries[data[0]] = [question[2:], query]
    questionsFile.close()
    queryFile.close()
    return queries


# asks the user which query they would like to execute and returns the results
def ask_the_user(queries):
    # print out the questions and their letter (ex. a,Top ten Athletes who the most medals for the Summer Games)
    for key in queries:
        print(key + ',' + queries[key][0])

    # possible letters that can be inputted
    possible_letters = ['a','b','c','d','e','f','g','h','i','j']
    letter = input('Enter the letter for the question you want to answer: ')
    while letter not in possible_letters:
        letter = input('Invalid Entry. Try again: ')

    return letter


# run the query and get the result from sql
def questionAns(cursor, queries, letter):
    # execute the sql query
    cursor.execute(queries[letter][1])
    result = cursor.fetchone()

    # use the BeautifulTable library to print the table
    table = BeautifulTable()
    for row in result:
        table.append_row(row)

    print(table)


def main():
    DB_NAME = 'OlympicMedals'
    cursor, connection = connectToMySQL()
    cursor.execute("USE {}".format(DB_NAME))

    # ask the user which question they want answered and return the output from sql
    queries = createQueries()
    letter = ask_the_user(queries)
    questionAns(cursor, queries, letter)

    connection.commit()
    cursor.close()
    connection.close()


main()