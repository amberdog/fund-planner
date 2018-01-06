#! /usr/bin/python

import calendar
import sqlite3
from enum import Enum

class Month(Enum):
    # Start at 1 to match the calendar package
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __str__(self):
        return self.name.capitalize()

class Recurring(Enum):
    NEVER = 0
    DAILY = 1
    MONTHLY = 2
    YEARLY = 3

    def __str__(self):
        return self.name.capitalize()


class AccountAdjustment:
    def __init__(self, accountId, name, year, month, day, recurring, amount,
            rowId=None):
        self.rowId = rowId
        self.accountId = accountId
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.recurring = recurring
        self.amount = amount

    def __str__(self):
        return " ".join(str(val) for val in self.asTuple())

    def asTuple(self):
        return (self.rowId, self.accountId, self.name, self.year, self.month,
                self.day, self.recurring, self.amount)


class AccountAdjustmentsTable:
    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        self.cursor = self.connection.cursor()

    def createTable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS AccountAdjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            accountId INTEGER NOT NULL,
            name STRING NOT NULL,
            year INTEGER,
            month INTEGER,
            day INTEGER NOT NULL,
            recurring SMALLINT NOT NULL,
            amount MONEY NOT NULL
            )""")
        self.connection.commit()

    def buildAccountAdjustmentFromRow(self, row, expectedMonth=None, expectedYear=None):
        rowId = row[0]
        accountId = row[1]
        name = row[2]
        year = row[3]
        month = row[4]
        day = row[5]
        recurring = row[6]
        amount = row[7]

        # Convert the month number to the enum
        if month != None:
            month = Month(month)
        else:
            month = expectedMonth

        if year == None:
            year = expectedYear

        if month and year:
            # Adjust the day to the last day of the month if it's out of range.
            lastDayOfMonth = calendar.monthrange(year, month.value)[1]
            if day > lastDayOfMonth:
                day = lastDayOfMonth

        return AccountAdjustment(rowId=rowId, accountId=accountId, name=name,
                year=year, month=month, day=day, recurring=Recurring(recurring), amount=amount)

    def readAll(self):
        for row in self.cursor.execute("""SELECT * FROM AccountAdjustments"""):
            yield self.buildAccountAdjustmentFromRow(row)

    def getAdjustments(self, month, year):
        monthNumber = month.value
        self.cursor.execute("""SELECT * FROM AccountAdjustments where (month=? \
                AND year=?) OR (month=? AND recurring=?) OR (recurring=?) ORDER BY day""",
                (monthNumber, year, monthNumber, Recurring.YEARLY.value, Recurring.MONTHLY.value))
        rows = self.cursor.fetchall()

        adjustments = []
        for row in rows:
            adjustments.append(self.buildAccountAdjustmentFromRow(row, month, year))
        return adjustments

    def addNew(self, account):
        month = None
        if account.month:
            month = account.month.value

        row = (account.accountId, account.name, account.year, month, account.day,
                account.recurring.value, account.amount)
        self.cursor.execute("""INSERT INTO AccountAdjustments(accountId, name,
                year, month, day, recurring, amount) VALUES (?,?,?,?,?,?,?)""", row)
        self.connection.commit()

    def count(self):
        self.cursor.execute("""SELECT COUNT(*) FROM AccountAdjustments""")
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()
