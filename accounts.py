#! /usr/bin/python

import sqlite3

class Account:
    def __init__(self, name, currentAmount, rowId=None):
        self.rowId = rowId
        self.name = name
        self.currentAmount = currentAmount

    def getName(self):
        return self.name

    def getCurrentAmount(self):
        return self.currentAmount


class AccountsTable:
    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        self.cursor = self.connection.cursor()

    def createTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name STRING,
            currentAmount MONEY NOT NULL
            )""")
        self.connection.commit()

    def readAll(self):
        for row in self.cursor.execute("SELECT * FROM Accounts"):
            rowId = row[0]
            name = row[1]
            currentAmount = row[2]
            yield Account(rowId=rowId, name=name, currentAmount=currentAmount)

    def addNew(self, account):
        row = (account.name, account.currentAmount)
        self.cursor.execute("INSERT INTO Accounts(name, currentAmount) VALUES (?,?)", row)
        self.connection.commit()

    def count(self):
        self.cursor.execute("SELECT COUNT(*) FROM Accounts")
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()
