<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) > The Document Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A43A20B7-A73A-4BBC-B871-B8E6B9D1006C.htm -->

# The Document Object (.NET)

The Document object, which is actually an AutoCAD drawing, is part of the DocumentCollection object. You use the DocumentExtension and DocumentCollectionExtention objects to create, open, and close drawing files. A Document object provides access to the Database object which contains all of the graphical and most of the non-graphical AutoCAD objects. 

Along with the Database object, the Document object provides access to the status bar, the window the document is opened in, the Editor and TransactionManager objects. The Editor object provides access to functions used to obtain input from the user in the form of a point or an entered string or numeric value. 

The TransactionManager object is used to access multiple database objects under a single operation known as a _transaction_. Transactions can be nested, and when you are done with a transaction you can commit or abort the changes made.
