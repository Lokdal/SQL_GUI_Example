# Steps
# 1 Connect to a database
# 2 Create a cursor object
# 3 Make a SQL query
# 4 Commit the changes
# 5 Close the connection

import sqlite3
import exceptions as Ex

TABLE_NAME = "store"


def fCreateTable():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS " + TABLE_NAME
                   + " (id INTEGER PRIMARY KEY,"
                   + " title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
    connection.commit()
    connection.close()


# This function only returns id and is used for Add, Delete and Update
def fCheckForMultipleEntries(title, author, year, isbn):
    connection = sqlite3.connect("books.db")
    connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    matches = cursor.execute(
        "SELECT id FROM " + TABLE_NAME + " WHERE title=? AND author=? "
        + "AND year=? AND isbn=?",
        (title, author, year, isbn)).fetchall()
    editions = cursor.execute(
        "SELECT id FROM " + TABLE_NAME + " WHERE title=? AND author=? "
        + "AND NOT year=? AND NOT isbn=?",
        (title, author, year, isbn)).fetchall()
    if len(editions) > 0:
        raise Ex.EditionExistsError
    elif len(matches) > 1:
        raise Ex.MultipleIdenticalEntriesError
    else:
        return(matches)


# If some fields are left blank, fills them with wildcards.
# This function allows multiple results and returns the entire entry/ies
def fSearchEntry(title, author, year, isbn):
    query = ""
    args = ()
    for name in ['title', 'author', 'year', 'isbn']:
        if eval(name) != "":
            args = args + (eval(name), )
            query += name + "=? AND "
    query = query[:-5]
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    books = cursor.execute(
        "SELECT * FROM " + TABLE_NAME + " WHERE " + query, args).fetchall()
    connection.close()
    return(books)


# Cannot be called if a field is left empty.
# Will only return exact matches
def fAddEntry(title, author, year, isbn):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO " + TABLE_NAME + " VALUES (NULL, ?, ?, ?, ?)",
                   (title, author, year, isbn))
    connection.commit()
    connection.close()


def fUpdateEntry(id, title, author, year, isbn):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE " + TABLE_NAME
        + " SET title=?, author=?, year=?, isbn=? WHERE id=?",
        (title, author, year, isbn, id))
    connection.commit()
    connection.close()


def fDeleteEntry(id, title, author, year, isbn):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    connection.row_factory = lambda cursor, row: row[0]
    args_book = cursor.execute(
        "SELECT id FROM " + TABLE_NAME + " WHERE title=? AND author=? "
        + "AND year=? AND isbn=?", (title, author, year, isbn)).fetchall()
    try:
        if (len(args_book) == 1) & (args_book[0] == id):
            cursor.execute("DELETE FROM " + TABLE_NAME + " WHERE id=?", (id, ))
        else:
            raise IndexError
    except IndexError:
        print("Properties entered do not match the selected entry.")
    connection.commit()
    connection.close()


def fSelectAll():
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    books = cursor.execute("SELECT * FROM " + TABLE_NAME).fetchall()
    connection.close()
    return(books)


fCreateTable()
