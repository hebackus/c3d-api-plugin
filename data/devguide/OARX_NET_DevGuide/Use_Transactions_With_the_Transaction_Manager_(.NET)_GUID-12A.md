<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Use Transactions With the Transaction Manager (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-12ADA0F2-C44D-4D88-B248-1803D39DF3AA.htm -->

# Use Transactions With the Transaction Manager (.NET)

Transactions are used to group multiple operations on multiple objects together as a single operation. Transactions are started and managed through the Transaction Manager. Once a transaction is started, you can then use the GetObject function to open an object. 

As you work with objects opened with GetObject, the Transaction manager keeps track of the changes that are being made to the object. Any new objects that you create and add to the database should be added to a transaction as well with the AddNewlyCreatedDBObject function. Once the objects have been edited or added to the database, you can save the changes made to the database and close all the open objects with the Commit function on the Transaction object created with the Transaction Manager. Once you are finished with a transaction, call the Dispose function close the transaction.
