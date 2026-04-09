<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Copy Objects (.NET) > Copy Objects Between Databases (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E02A8AAF-61FF-4C72-8960-0AEEBBEC2594.htm -->

# Copy Objects Between Databases (.NET)

You can copy objects between two databases with the WblockCloneObjects method. The WblockCloneObjects method is a member of the Database object. 

Note: Do not use the CopyFrom method to copy objects between two databases. 

The WblockCloneObjects method requires the following parameters: 

  * **ObjectIdCollection** \- List of objects to be cloned. 
  * **ObjectId** \- ObjectId of the new parent object for the objects being cloned. 
  * **IdMapping** \- Data structure of the current and new ObjectIds for the objects being cloned. 
  * **DuplicateRecordCloning** \- Determines how duplicate objects should be handled. 
  * **Defer Translation** \- Controls if object ids should be translated. 

## Copy an object from one database to another

This example creates two Circle objects, then uses the WblockCloneObjects method to copy the circles into a new drawing. The example also creates a new drawing using the _acad.dwt_ file before the circles are copied. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CopyObjectsBetweenDatabases", CommandFlags.Session)]
    public static void CopyObjectsBetweenDatabases()
    {
        ObjectIdCollection acObjIdColl = new ObjectIdCollection();
    
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Lock the current document
        using (DocumentLock acLckDocCur = acDoc.LockDocument())
        {
            // Start a transaction
            using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
            {
                // Open the Block table record for read
                BlockTable acBlkTbl;
                acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                             OpenMode.ForRead) as BlockTable;
    
                // Open the Block table record Model space for write
                BlockTableRecord acBlkTblRec;
                acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                                OpenMode.ForWrite) as BlockTableRecord;
    
                // Create a circle that is at (0,0,0) with a radius of 5
                using (Circle acCirc1 = new Circle())
                {
                    acCirc1.Center = new Point3d(0, 0, 0);
                    acCirc1.Radius = 5;
    
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acCirc1);
                    acTrans.AddNewlyCreatedDBObject(acCirc1, true);
    
                    // Create a circle that is at (0,0,0) with a radius of 7
                    using (Circle acCirc2 = new Circle())
                    {
                        acCirc2.Center = new Point3d(0, 0, 0);
                        acCirc2.Radius = 7;
    
                        // Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc2);
                        acTrans.AddNewlyCreatedDBObject(acCirc2, true);
    
                        // Add all the objects to copy to the new document
                        acObjIdColl = new ObjectIdCollection();
                        acObjIdColl.Add(acCirc1.ObjectId);
                        acObjIdColl.Add(acCirc2.ObjectId);
                    }
                }
    
                // Save the new objects to the database
                acTrans.Commit();
            }
    
            // Unlock the document
        }
    
        // Change the file and path to match a drawing template on your workstation
        string sLocalRoot = Application.GetSystemVariable("LOCALROOTPREFIX") as string;
        string sTemplatePath = sLocalRoot + "Template\\acad.dwt";
    
        // Create a new drawing to copy the objects to
        DocumentCollection acDocMgr = Application.DocumentManager;
        Document acNewDoc = acDocMgr.Add(sTemplatePath);
        Database acDbNewDoc = acNewDoc.Database;
    
        // Lock the new document
        using (DocumentLock acLckDoc = acNewDoc.LockDocument())
        {
            // Start a transaction in the new database
            using (Transaction acTrans = acDbNewDoc.TransactionManager.StartTransaction())
            {
                // Open the Block table for read
                BlockTable acBlkTblNewDoc;
                acBlkTblNewDoc = acTrans.GetObject(acDbNewDoc.BlockTableId,
                                                   OpenMode.ForRead) as BlockTable;
    
                // Open the Block table record Model space for read
                BlockTableRecord acBlkTblRecNewDoc;
                acBlkTblRecNewDoc = acTrans.GetObject(acBlkTblNewDoc[BlockTableRecord.ModelSpace],
                                                      OpenMode.ForRead) as BlockTableRecord;
    
                // Clone the objects to the new database
                IdMapping acIdMap = new IdMapping();
                acCurDb.WblockCloneObjects(acObjIdColl, acBlkTblRecNewDoc.ObjectId, acIdMap,
                                           DuplicateRecordCloning.Ignore, false);
    
                // Save the copied objects to the database
                acTrans.Commit();
            }
    
            // Unlock the document
        }
    
        // Set the new document current
        acDocMgr.MdiActiveDocument = acNewDoc;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CopyObjectsBetweenDatabases", CommandFlags.Session)> _
    Public Sub CopyObjectsBetweenDatabases()
        Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
    
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Lock the current document
        Using acLckDocCur As DocumentLock = acDoc.LockDocument()
    
            '' Start a transaction
            Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
                '' Open the Block table for read
                Dim acBlkTbl As BlockTable
                acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
                '' Open the Block table record Model space for write
                Dim acBlkTblRec As BlockTableRecord
                acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                                OpenMode.ForWrite)
    
                '' Create a circle that is at (0,0,0) with a radius of 5
                Using acCirc1 As Circle = New Circle()
                    acCirc1.Center = New Point3d(0, 0, 0)
                    acCirc1.Radius = 5
    
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acCirc1)
                    acTrans.AddNewlyCreatedDBObject(acCirc1, True)
    
                    '' Create a circle that is at (0,0,0) with a radius of 7
                    Using acCirc2 As Circle = New Circle()
                        acCirc2.Center = New Point3d(0, 0, 0)
                        acCirc2.Radius = 7
    
                        '' Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc2)
                        acTrans.AddNewlyCreatedDBObject(acCirc2, True)
    
                        '' Add all the objects to copy to the new document
                        acObjIdColl = New ObjectIdCollection()
                        acObjIdColl.Add(acCirc1.ObjectId)
                        acObjIdColl.Add(acCirc2.ObjectId)
                    End Using
                End Using
    
                '' Save the new objects to the database
                acTrans.Commit()
            End Using
    
            '' Unlock the document
        End Using
    
        '' Change the file and path to match a drawing template on your workstation
        Dim sLocalRoot As String = Application.GetSystemVariable("LOCALROOTPREFIX")
        Dim sTemplatePath As String = sLocalRoot + "Template\acad.dwt"
    
        '' Create a new drawing to copy the objects to
        Dim acDocMgr As DocumentCollection = Application.DocumentManager
        Dim acNewDoc As Document = DocumentCollectionExtension.Add(acDocMgr, sTemplatePath)
        Dim acDbNewDoc As Database = acNewDoc.Database
    
        '' Lock the new document
        Using acLckDoc As DocumentLock = acNewDoc.LockDocument()
    
            '' Start a transaction in the new database
            Using acTrans = acDbNewDoc.TransactionManager.StartTransaction()
    
                '' Open the Block table for read
                Dim acBlkTblNewDoc As BlockTable
                acBlkTblNewDoc = acTrans.GetObject(acDbNewDoc.BlockTableId, _
                                                   OpenMode.ForRead)
    
                '' Open the Block table record Model space for read
                Dim acBlkTblRecNewDoc As BlockTableRecord
                acBlkTblRecNewDoc = acTrans.GetObject(acBlkTblNewDoc(BlockTableRecord.ModelSpace), _
                                                      OpenMode.ForRead)
    
                '' Clone the objects to the new database
                Dim acIdMap As IdMapping = New IdMapping()
                acCurDb.WblockCloneObjects(acObjIdColl, acBlkTblRecNewDoc.ObjectId, acIdMap, _
                                           DuplicateRecordCloning.Ignore, False)
    
                '' Save the copied objects to the database
                acTrans.Commit()
            End Using
    
            '' Unlock the document
        End Using
    
        '' Set the new document current
        acDocMgr.MdiActiveDocument = acNewDoc
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CopyObjectsBetweenDatabases()
        Dim DOC0 As AcadDocument
        Dim circleObj1 As AcadCircle, circleObj2 As AcadCircle
        Dim centerPoint(0 To 2) As Double
        Dim radius1 As Double, radius2 As Double
        Dim objCollection(0 To 1) As Object
        Dim retObjects As Variant
     
        ' Define the Circle object
        centerPoint(0) = 0: centerPoint(1) = 0: centerPoint(2) = 0
        radius1 = 5#: radius2 = 7#
     
        ' Add two circles to the current drawing
        Set circleObj1 = ThisDrawing.ModelSpace.AddCircle _
                         (centerPoint, radius1)
        Set circleObj2 = ThisDrawing.ModelSpace.AddCircle _
                         (centerPoint, radius2)
     
        ' Save pointer to the current drawing
        Set DOC0 = ThisDrawing.Application.ActiveDocument
     
        ' Copy objects
        '
        ' First put the objects to be copied into a form compatible
        ' with CopyObjects
        Set objCollection(0) = circleObj1
        Set objCollection(1) = circleObj2
     
        ' Create a new drawing and point to its model space
        Dim Doc1MSpace As AcadModelSpace
        Dim DOC1 As AcadDocument
     
        Set DOC1 = Documents.Add
        Set Doc1MSpace = DOC1.ModelSpace
     
        ' Copy the objects into the model space of the new drawing. A
        ' collection of the new (copied) objects is returned.
        retObjects = DOC0.CopyObjects(objCollection, Doc1MSpace)
    End Sub
