<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Work With ObjectIds (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8D56532D-2B17-48D1-8C81-B4AD89603A1C.htm -->

# Work With ObjectIds (.NET)

Each object contained within a database is assigned several unique ids. The unique ways you can access objects are: 

  * Entity handle 
  * ObjectId 
  * Instance pointer 

The most common way to access an object is by its ObjectId. ObjectIds work well if your projects utilize both COM interop and the managed AutoCAD .NET API. If you create custom AutoLISP functions, you may need to work with entity handles. 

Handles are persistent between AutoCAD sessions, so they are the best way of accessing objects if you need to export drawing information to an external file which might later need to be used to update the drawing. The ObjectId of an object in a database exists only while the database is loaded into memory. Once the database is closed, the ObjectId assigned to an object no longer exist and maybe different the next time the database is opened. 

## Obtain an ObjectId

As you work with objects, you will need to obtain an ObjectId first before you can open the object to query or edit it. An ObjectId is assigned to an existing object in the database when the drawing file is opened, and new objects are assigned an ObjectId when they are first created. An ObjectId is commonly obtained for an existing object in the database by: 

  * Using a member property of the Database object, such as Clayer which retrieves the Object ID for the current layer 
  * Iterating a symbol table, such as the Layer symbol table 

## Open an Object

Once an Object Id is obtained, the GetObject function is used to open the object assigned the given Object Id. An object can be opened in one of the following modes: 

  * **Read**. Opens an object for read. 
  * **Write**. Opens an object for write if it is not already open. 
  * **Notify**. Opens an object for notification when it is closed, open for read, or open for write, but not when it is already open for notify. This mode is intended for use when an object might modify itself from within its own code, such as when defining a custom object which is not supported with the AutoCAD Managed .NET API. 

You should open an object in the mode that is best for the situation in which the object will be accessed. Opening an object for write introduces additional overhead than you might need due to the creation of undo records. If you are unsure if the object you are opening is the one you want to work with, you should open it for read and then upgrade the object from read to write mode. For more information on upgrading an object, see "Upgrade and Downgrade Open Objects (.NET)." 

Both the GetObject and Open functions return an object. When working with some programming languages, you will need to cast the returned value based on the variable the value is being assigned to. If you are using VB.NET, you do not need to worry about casting the return value as it is done for you. 

When working with the Dynamic Runtime Language (DLR), you do not need to worry about opening an object for read or write. The opening of an object is handled transparently for you, and so is the process of committing the changes made to an object without using transactions. 

The following examples show how to obtain the LayerTableRecord for Layer Zero of the current database. 

### C#

The following example manually disposes of the transaction after it is no longer needed. 
    
    
    Document acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    Transaction acTrans = acCurDb.TransactionManager.StartTransaction();
     
    LayerTableRecord acLyrTblRec;
    acLyrTblRec = acTrans.GetObject(acCurDb.LayerZero,
                                    OpenMode.ForRead) as LayerTableRecord;
     
    acTrans.Dispose();

The following example uses the Using statement to dispose of the transaction after it is no longer needed. The Using statement is the preferred coding style. 
    
    
    Document acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
    {
        LayerTableRecord acLyrTblRec;
        acLyrTblRec = acTrans.GetObject(acCurDb.LayerZero,
                                        OpenMode.ForRead) as LayerTableRecord;
    }

### VB.NET

The following example manually disposes of the transaction after it is no longer needed. 
    
    
    Dim acCurDb As Document = Application.DocumentManager.MdiActiveDocument.Database
    Dim acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
    Dim acLyrTblRec As LayerTableRecord
    acLyrTblRec = acTrans.GetObject(acCurDb.LayerZero, OpenMode.ForRead)
     
    acTrans.Dispose()

The following example uses the Using statement to dispose of the transaction after it is no longer needed. The Using statement is the preferred coding style. 
    
    
    Dim acCurDb As Document = Application.DocumentManager.MdiActiveDocument.Database
    Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
        Dim acLyrTblRec As LayerTableRecord
        acLyrTblRec = acTrans.GetObject(acCurDb.LayerZero, OpenMode.ForRead)
    End Using
