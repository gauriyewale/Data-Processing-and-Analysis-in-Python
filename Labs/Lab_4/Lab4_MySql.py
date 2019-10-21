#Used Python 2.7 as MySql 8.0.17 does not support 3.7
# coding: UTF-8


#Import packages
import mysql.connector
from mysql.connector import Error

'''
Definition of function to connect to database 'test'
Note: Had to use charset='latin1' as some characters were 
not getting inserted into the table due to latin characters.
'''
def connect_to_db():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='test',
                                             user='root',
                                             password='gauri5070',
                                             charset='latin1')

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select database();")
            db = cursor.fetchone()
            print("Your connected to database: ", db)
            return connection, cursor
    except Error as e:
        print("Error while connecting to MySQL", e)

'''
Definition of function to close the connection to database.
'''
def close_connection(connection, cursor): 
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

'''
Definition of function to insert data into database.
'''
def insert_data(cursor, docID, name, specialty, numReviews, city, state):
    
    sql = "INSERT INTO doctors (docID, name, specialty, numReviews, city, state) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (docID, name, specialty, numReviews, city, state)
    cursor.execute(sql, val)

'''
Definition of function execute following query:
1. Find the total number of doctors, the average number of reviews in the state of MD. 
(Use select statement with some functions like count() and avg())
'''
def func_query1(cursor):
    query1 = "SELECT count(name), avg(numReviews) FROM doctors WHERE state='MD'"
    cursor.execute(query1)
    query1 = cursor.fetchall()
    print("Count of doctors in Maryland is {} and average number of reviews is {}".format(query1[0][0],query1[0][1]))

'''
Definition of function execute following query:
2. Print out name and specialty about the top 10 doctors in terms of number of reviews in the state of MD. 
(Use select statement combined with order by)
'''
def func_query2(cursor):
    query2 = "SELECT name, specialty FROM doctors WHERE state='MD' ORDER BY numReviews DESC LIMIT 10;"
    cursor.execute(query2)
    query2 = cursor.fetchall()
    print("List of top 10 doctors and their specialties in terms of reviews in Maryland: ")
    for x in query2:
        print(x[0] +'\t\t'+ x[1])

'''
Definition of function execute following query:
3. For doctors without city or state information (denoted by a hyphen: ‘-’ in the text file),
please update their city or state to be: U. (Use update statement)
'''
def func_query3(cursor, connection):
    query_state = "UPDATE doctors SET state = 'U' WHERE state = '-'"
    cursor.execute(query_state)
    connection.commit()

    query_city = "UPDATE doctors SET city = 'U' WHERE city = '-'"
    cursor.execute(query_city)
    connection.commit()


'''
Main function definition

'''
def main():
    #Connect to database
    connection, cursor = connect_to_db()

    #Read the text file
    fh = open('doctors.txt')
    doctor_data = fh.readlines()

    #Create table doctors
    cursor.execute("CREATE TABLE doctors (docID INT(11) PRIMARY KEY, name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_general_ci, specialty VARCHAR(50), numReviews INT(11), city TINYTEXT, state VARCHAR(2))")

    #Iterate over the text file and add each entry to the database
    for i in range(0, len(doctor_data)):
        doctor_data[i] = doctor_data[i].strip().split(',')
        #print(doctor_data[i][0], doctor_data[i][1], doctor_data[i][2], doctor_data[i][3], doctor_data[i][4], doctor_data[i][5])
        insert_data(cursor, doctor_data[i][0], doctor_data[i][1], doctor_data[i][2], doctor_data[i][3], doctor_data[i][4], doctor_data[i][5])
        #print(doctor_data[i][0])

    #Commit changes made to the table
    connection.commit()

    #Call functions to execute the queries
    func_query1(cursor)
    func_query2(cursor)
    func_query3(cursor, connection)

    #Close the connection
    close_connection(connection, cursor)

if __name__ == '__main__':

    main()
