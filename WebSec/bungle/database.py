import os, sys
import pymysql as mdb
from bottle import FormsDict
from hashlib import md5

# connection to database project2
def connect():
    """
    Creates a connection object to the MySQL database.
    @return a mysqldb connection object.
    """

    #TODO: 1 of 6 fill out MySQL connection parameters. 
    # Use the netid and given password of the repo you are committing your solution to.
    # See the file we gave you called dbrw.secret in your repo.
    # Do not change this value - we use it when grading. 

    # Use the password value from the `dbrw.secret` file.
    return mdb.connect(host='localhost', user='yclai4', password='423510c156a3f2680ee62f3fff42ca1c05fa87b05551f18fa5130b5dfe1017cc', db='project2')

def createUser(username, password):
    """
    Creates a row in table named `users`
    @param username: username of user
    @param password: password of user
    """

    db_rw = connect()
    cur = db_rw.cursor()
    password_hash = str(md5(password.encode('utf-8')).hexdigest())
    #TODO 2 of 6. Use cur.execute() to insert a new row into the users table containing the username, password, and passwordhash
    sql_command = f"INSERT INTO users (username, password, passwordhash) VALUES ('{username}', '{password}', '{password_hash}')"
    cur.execute(sql_command)
    db_rw.commit()

def validateUser(username, password):
    """ validates if username,password pair provided by user is correct or not
    @param username: username of user
    @param password: password of user
    @return True if validation was successful, False otherwise.
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO 3 of 6. Use cur.execute() to select the appropriate user record (if it exists)
    sql_command = f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'"
    cur.execute(sql_command)
    if cur.rowcount < 1:
        return False
    return True

def fetchUser(username):
    """ checks if there exists given username in table users or not
    if user exists return (id, username) pair
    if user does not exist return None
    @param username: the username of a user
    @return The row which has username is equal to provided input
    """

    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    #TODO 4 of 6. Use cur.execute() to fetch the row with this username from the users table, if it exists
    sql_command = f"SELECT id, username FROM users WHERE username = '{username}'"
    cur.execute(sql_command)
    if cur.rowcount < 1:
        return None    
    return FormsDict(cur.fetchone())

def addHistory(user_id, query):
    """ adds a query from user with id=user_id into table named history
    @param user_id: integer id of user
    @param query: the query user has given as input
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO 5 of 6. Use cur.execute() to add a row to the history table containing the correct user_id and query
    sql_command = f"INSERT INTO history (user_id, query) VALUES ('{user_id}', '{query}')"
    cur.execute(sql_command)
    db_rw.commit()

def getHistory(user_id):
    """ grabs last 15 queries made by user with id=user_id from
    table named history in descending order of when the searches were made
    @param user_id: integer id of user
    @return a first column of a row which MUST be query
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO 6 of 6. Use cur.execute() to fetch the most recent 15 queries from this user (including duplicates). 
    # Note: Make sure the query text is at index 0 in the returned rows. 
    # Otherwise you will get an error when the templating engine tries to use this object to build the HTML reply.
    sql_command = f"SELECT query FROM history WHERE user_id = '{user_id}' ORDER BY id DESC LIMIT 15"
    cur.execute(sql_command)
    rows = cur.fetchall()
    return [row[0] for row in rows]
