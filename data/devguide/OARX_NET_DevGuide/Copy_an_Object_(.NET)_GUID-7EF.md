<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Copy Objects (.NET) > Copy an Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7EF7D821-473B-4F05-A98C-AEEC9F86A871.htm -->

# Copy an Object (.NET)

To copy an object, use the Clone method provided for that object. This method creates a new object that is a duplicate of the original object in the same database. Once the duplicate object is created, you can then modify it prior to adding or appending it to the database. If you do not transform the object or change its position, the new object will be located in the same position as the original. In addition to creating a new object with the Clone method, the CopyFrom method can be used to copy properties from one object to another object. 

If you have a large number of objects you might want to copy, you can add each of the object ids to an ObjectIdCollection object and then iterate each object id in the collection. As you iterate each object id, you can then use the Clone function after the open is open for read and then add or append the new object to the database. 

## Copy a single object

The following example creates a new circle and then creates a direct copy of the circle to create a second circle. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("SingleCopy")]
    public static void SingleCopy()
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
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle that is at 2,3 with a radius of 4.25
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 3, 0);
                acCirc.Radius = 4.25;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                // Create a copy of the circle and change its radius
                Circle acCircClone = acCirc.Clone() as Circle;
                acCircClone.Radius = 1;
    
                // Add the cloned circle
                acBlkTblRec.AppendEntity(acCircClone);
                acTrans.AddNewlyCreatedDBObject(acCircClone, true);
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("SingleCopy")> _
    Public Sub SingleCopy()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle that is at 2,3 with a radius of 4.25
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 3, 0)
                acCirc.Radius = 4.25
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Create a copy of the circle and change its radius
                Dim acCircClone As Circle = acCirc.Clone()
                acCircClone.Radius = 1
    
                '' Add the cloned circle
                acBlkTblRec.AppendEntity(acCircClone)
                acTrans.AddNewlyCreatedDBObject(acCircClone, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SingleCopy()
        ' Define the Circle object
        Dim centerPoint(0 To 2) As Double
        centerPoint(0) = 2: centerPoint(1) = 3: centerPoint(2) = 0
     
        ' Define the radius for the initial circle
        Dim radius As Double
        radius = 4.25
     
        ' Define the radius for the copied circle
        Dim radiusCopy As Double
        radiusCopy = 1#
     
        ' Add the new circle to model space
        Dim circleObj As AcadCircle
        Set circleObj = ThisDrawing.ModelSpace.AddCircle(centerPoint, radius)
     
        ' Create a copy of the circle
        Dim circleObjCopy As AcadCircle
        Set circleObjCopy = circleObj.Copy()
        circleObjCopy.radius = radiusCopy
    End Sub

## Copy multiple objects

The following example uses an ObjectIdCollection object to track the objects that should be copied. Once the object ids are added to the collection, the collection is iterated and new objects are created by using the Clone method and then are added to Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("MultipleCopy")]
    public static void MultipleCopy()
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
    
                    // Add all the objects to clone
                    DBObjectCollection acDBObjColl = new DBObjectCollection();
                    acDBObjColl.Add(acCirc1);
                    acDBObjColl.Add(acCirc2);
    
                    foreach (Entity acEnt in acDBObjColl)
                    {
                        Entity acEntClone;
                        acEntClone = acEnt.Clone() as Entity;
                        acEntClone.ColorIndex = 1;
    
                        // Create a matrix and move each copied entity 15 units
                        acEntClone.TransformBy(Matrix3d.Displacement(new Vector3d(15, 0, 0)));
    
                        // Add the cloned object
                        acBlkTblRec.AppendEntity(acEntClone);
                        acTrans.AddNewlyCreatedDBObject(acEntClone, true);
                    }
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("MultipleCopy")> _
    Public Sub MultipleCopy()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
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
    
                    '' Add all the objects to clone
                    Dim acDBObjColl As DBObjectCollection = New DBObjectCollection()
                    acDBObjColl.Add(acCirc1)
                    acDBObjColl.Add(acCirc2)
    
                    For Each acEnt As Entity In acDBObjColl
                        Dim acEntClone As Entity
                        acEntClone = acEnt.Clone()
                        acEntClone.ColorIndex = 1
    
                        '' Create a matrix and move each copied entity 15 units
                        acEntClone.TransformBy(Matrix3d.Displacement(New Vector3d(15, 0, 0)))
    
                        '' Add the cloned object
                        acBlkTblRec.AppendEntity(acEntClone)
                        acTrans.AddNewlyCreatedDBObject(acEntClone, True)
                    Next
                End Using
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MultipleCopy()
        ' Define the Circle object
        Dim centerPoint(0 To 2) As Double
        centerPoint(0) = 0: centerPoint(1) = 0: centerPoint(2) = 0
     
        Dim radius1 As Double, radius2 As Double
        radius1 = 5#: radius2 = 7#
     
        ' Add two circles to the current drawing
        Dim circleObj1 As AcadCircle, circleObj2 As AcadCircle
        Set circleObj1 = ThisDrawing.ModelSpace.AddCircle _
                                                (centerPoint, radius1)
     
        Set circleObj2 = ThisDrawing.ModelSpace.AddCircle _
                                                (centerPoint, radius2)
     
        ' First put the objects to be copied into a form compatible
        ' with CopyObjects
        Dim objCollection(0 To 1) As Object
        Set objCollection(0) = circleObj1
        Set objCollection(1) = circleObj2
     
        ' Copy the objects into the model space. A
        ' collection of the new (copied) objects is returned.
        Dim retObjects As Variant
        retObjects = ThisDrawing.CopyObjects(objCollection)
     
        Dim ptFrom(0 To 2) As Double
        ptFrom(0) = 0: ptFrom(1) = 0: ptFrom(2) = 0
     
        Dim ptTo(0 To 2) As Double
        ptTo(0) = 15: ptTo(1) = 0: ptTo(2) = 0
     
        Dim nCount As Integer
        For nCount = 0 To UBound(retObjects)
             Dim entObj As AcadEntity
             Set entObj = retObjects(nCount)
     
             entObj.color = acRed
             entObj.Move ptFrom, ptTo
        Next
    End Sub
