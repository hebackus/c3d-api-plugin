<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Lock and Unlock a Document (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A2CD7540-69C5-4085-BCE8-2A8ACE16BFDD.htm -->

# Lock and Unlock a Document (.NET)

Requests to modify objects or access AutoCAD can occur in any context, and coming from any number of applications. To prevent conflicts with other requests, you are responsible for locking a document before you modify it. Failure to lock the document in certain contexts will cause a lock violation during the modification of the database. You want to lock the document when your application: 

  * Interacts with AutoCAD from a modeless dialog box 
  * Accesses a loaded document other than the current document 
  * Used as a COM server 
  * Registers a command with the Session command flag 

For example, when adding an entity to Model or Paper space in a document other than the current document, the document needs to be locked. You use the LockDocument method of the Database object you want to lock. When the LockDocument method is called, a DocumentLock object is returned. 

Once you are done modifying the locked database, you need to unlock the database. To unlock the database, you call the Dispose method of the DocumentLock object. You can also use the Using statement with the DocumentLock object, once the Using statement ends the database is unlocked. 

Note: When working in the context of a command that does not use the Session command flag, you do not need to lock the database for the current document before it is modified. 

## Lock a database before modifying an object

This example creates a new document and then draws a circle in it. After the document is created, the database for the new document is locked and then a circle is added to it. After the circle is added, the database is unlocked and the associated document window is set current. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("LockDoc", CommandFlags.Session)]
    public static void LockDoc()
    {
        // Create a new drawing
        DocumentCollection acDocMgr = Application.DocumentManager;
        Document acNewDoc = acDocMgr.Add("acad.dwt");
        Database acDbNewDoc = acNewDoc.Database;
    
        // Lock the new document
        using (DocumentLock acLckDoc = acNewDoc.LockDocument())
        {
            // Start a transaction in the new database
            using (Transaction acTrans = acDbNewDoc.TransactionManager.StartTransaction())
            {
                // Open the Block table for read
                BlockTable acBlkTbl;
                acBlkTbl = acTrans.GetObject(acDbNewDoc.BlockTableId,
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
    
                // Save the new object to the database
                acTrans.Commit();
            }
    
            // Unlock the document
        }
    
        // Set the new document current
        acDocMgr.MdiActiveDocument = acNewDoc;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("LockDoc", CommandFlags.Session)> _
    Public Sub LockDoc()
        '' Create a new drawing
        Dim acDocMgr As DocumentCollection = Application.DocumentManager
        Dim acNewDoc As Document = DocumentCollectionExtension.Add(acDocMgr, "acad.dwt")
        Dim acDbNewDoc As Database = acNewDoc.Database
    
        '' Lock the new document
        Using acLckDoc As DocumentLock = acNewDoc.LockDocument()
    
            '' Start a transaction in the new database
            Using acTrans As Transaction = acDbNewDoc.TransactionManager.StartTransaction()
    
                '' Open the Block table for read
                Dim acBlkTbl As BlockTable
                acBlkTbl = acTrans.GetObject(acDbNewDoc.BlockTableId, _
                                             OpenMode.ForRead)
    
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
    
                '' Save the new object to the database
                acTrans.Commit()
            End Using
    
            '' Unlock the document
        End Using
    
        '' Set the new document current
        acDocMgr.MdiActiveDocument = acNewDoc
    End Sub
