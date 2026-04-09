<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Use Transactions With the Transaction Manager (.NET) > Use Transactions to Access and Create Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-50FD6118-B2D1-4313-A7D6-830794DFDEFA.htm -->

# Use Transactions to Access and Create Objects (.NET)

The Transaction Manager is accessed from the TransactionManager property of the current database. Once a reference to the Transaction Manager is made, you can use one of the following methods to start or obtain a transaction: 

  * **StartTransaction** – Starts a new transaction by creating a new instance of a Transaction object. Use this method when you need to write to an object multiple times and control how the changes can be rolled back through the use of different nesting levels. 
  * **StartOpenCloseTransation** – Creates an OpenCloseTransaction object, which behaves similar to a Transaction object, that wraps the Open and Close methods of an object making it easier to close all opened objects instead of having to explicitly close each opened object. Recommended for use in support or utility functions that might be called an unknown number of times, and used when working with most event handlers. 

Once you have a Transaction or OpenCloseTransaction object, use the GetObject method to open an object stored in the database for read or write. The GetObject method returns a DBObject which can be cast to the actual object type it represents. 

All open objects opened during a transaction are closed at the end of the transaction. To end a transaction, call the Dispose method of a transaction object. If you use the Using and End Using keywords to indicate the start and end of a transaction, you do not need to call the Dispose method. 

Prior to disposing of a transaction, you should commit any changes made with the Commit method. If the changes are not committed before a transaction is disposed, any changes made are rolled back to the state they were in prior to the start of the transaction. 

More than one transaction can be started. The number of active transactions can be retrieved with the NumberOfActiveTransactions property of the TransactionManager object while the top most or latest transaction can be retrieved with the TopTransaction property. 

Transactions can be nested one inside of another in order to roll back some of the changes made during the execution of a routine. 

## Query objects

The following example demonstrates how to open and read objects within using a transaction. You use the GetObject method to first open the BlockTable and then the Model space record. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("StartTransactionManager")]
    public static void StartTransactionManager()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
     
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
     
            // Open the Block table record Model space for read
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForRead) as BlockTableRecord;
     
            // Step through the Block table record
            foreach (ObjectId asObjId in acBlkTblRec)
            {
                acDoc.Editor.WriteMessage("\nDXF name: " + asObjId.ObjectClass.DxfName);
                acDoc.Editor.WriteMessage("\nObjectID: " + asObjId.ToString());
                acDoc.Editor.WriteMessage("\nHandle: " + asObjId.Handle.ToString());
                acDoc.Editor.WriteMessage("\n");
            }
     
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("StartTransactionManager")> _
    Public Sub StartTransactionManager()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
     
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
     
            '' Open the Block table record Model space for read
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForRead)
       
            '' Step through the Block table record
            For Each acObjId As ObjectId In acBlkTblRec
                acDoc.Editor.WriteMessage(vbLf & "DXF name: " & acObjId.ObjectClass().DxfName)
                acDoc.Editor.WriteMessage(vbLf & "ObjectID: " & acObjId.ToString())
                acDoc.Editor.WriteMessage(vbLf & "Handle: " & acObjId.Handle.ToString())
                acDoc.Editor.WriteMessage(vbLf)
            Next
     
            '' Dispose of the transaction
        End Using
    End Sub

## Add a new object to the database

The following example demonstrates how to add a circle object to the database with in a transaction. You use the GetObject method to first open the BlockTable for read and then the Model space record for write. After Model space is opened for write, you use the AppendEntity and AddNewlyCreatedDBObject function to append the new Circle object to Model space as well as the transaction. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddNewCircleTransaction")]
    public static void AddNewCircleTransaction()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartOpenCloseTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle with a radius of 3 at 5,5
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(5, 5, 0);
                acCirc.Radius = 3;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddNewCircleTransaction")> _
    Public Sub AddNewCircleTransaction()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartOpenCloseTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle with a radius of 3 at 5,5
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(5, 5, 0)
                acCirc.Radius = 3
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub
