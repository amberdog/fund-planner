#! /usr/bin/python

from accounts import AccountsTable, Account
from accountAdjustments import AccountAdjustmentsTable, AccountAdjustment, Month, Recurring
from prettytable import PrettyTable

def addDefaultAccounts():
    if accountsTable.count() > 0:
        return

    checking = Account(name='Checking', currentAmount=123)
    savings = Account(name='Savings', currentAmount=123)

    accountsTable.addNew(checking)
    accountsTable.addNew(savings)

def addTestValues():
    if accountAdjustmentsTable.count() > 0:
        return

    checkingId = 1
    # One-time adjustments
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name="Valentine's Day Dinner", year=2018, month=Month.FEBRUARY, day=14, recurring=Recurring.NEVER, amount=-80))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Thanksgiving Dinner', year=2018, month=Month.NOVEMBER, day=20, recurring=Recurring.NEVER, amount=-50))

    # Monthly adjustments
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Mortgage', year=None, month=None, day=3, recurring=Recurring.MONTHLY, amount=-2345.00))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Credit Card', year=None, month=None, day=5, recurring=Recurring.MONTHLY, amount=-1234))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Insurance', year=None, month=None, day=19, recurring=Recurring.MONTHLY, amount=-106.66))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Job Income', year=None, month=None, day=15, recurring=Recurring.MONTHLY, amount=3000))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Job Income', year=None, month=None, day=31, recurring=Recurring.MONTHLY, amount=3000))

    # Yearly adjustments
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Property Taxes', year=None, month=Month.NOVEMBER, day=1, recurring=Recurring.YEARLY, amount=-2000))
    accountAdjustmentsTable.addNew(AccountAdjustment(accountId=checkingId,
        name='Property Taxes', year=None, month=Month.FEBRUARY, day=1, recurring=Recurring.YEARLY, amount=-2000))


dbName = 'AccountExpectationsDB'
accountsTable = AccountsTable(dbName)
accountAdjustmentsTable = AccountAdjustmentsTable(dbName)

accountsTable.createTable()
accountAdjustmentsTable.createTable()
addDefaultAccounts()
addTestValues()

t = PrettyTable(['ID', 'Name', 'Amount'])
for account in accountsTable.readAll():
    t.add_row((account.rowId, account.getName(), account.getCurrentAmount()))
print 'Accounts'
print t

t = PrettyTable(['ID', 'Account ID', 'Name', 'Year', 'Month', 'Day', 'Recurring', 'Adjustment'])
for accountAdjustment in accountAdjustmentsTable.readAll():
    t.add_row(accountAdjustment.asTuple())
print '\nAccount Adjustments'
print t

t = PrettyTable(['ID', 'Account ID', 'Name', 'Year', 'Month', 'Day', 'Recurring', 'Adjustment'])
for accountAdjustment in accountAdjustmentsTable.getAdjustments(Month.NOVEMBER, 2018):
    t.add_row(accountAdjustment.asTuple())
print '\nAccount Adjustments for November'
print t

t = PrettyTable(['ID', 'Account ID', 'Name', 'Year', 'Month', 'Day', 'Recurring', 'Adjustment'])
for accountAdjustment in accountAdjustmentsTable.getAdjustments(Month.FEBRUARY, 2018):
    t.add_row(accountAdjustment.asTuple())
print '\nAccount Adjustments for February'
print t

accountsTable.close()
accountAdjustmentsTable.close()
