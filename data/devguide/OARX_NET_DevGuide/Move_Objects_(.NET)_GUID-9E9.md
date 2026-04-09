<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Transform Objects (.NET) > Move Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9E9D7A74-4FE7-4E57-B9CB-BA4712B364ED.htm -->

# Move Objects (.NET)

You can move all drawing objects and attribute reference objects along a specified vector. 

To move an object, use the Displacement function of a transformation matrix. This function requires a Vector3d object as input. If you do not know the vector that you need, you can create a Point3d object and then use the GetVectorTo method to return the vector between two points. The displacement vector indicates how far the given object is to be moved and in what direction. 

## Move a circle along a vector

This example creates a circle and then moves that circle two units along the _X_ axis. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("MoveObject")]
    public static void MoveObject()
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
    
            // Create a circle that is at 2,2 with a radius of 0.5
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 0.5;
    
                // Create a matrix and move the circle using a vector from (0,0,0) to (2,0,0)
                Point3d acPt3d = new Point3d(0, 0, 0);
                Vector3d acVec3d = acPt3d.GetVectorTo(new Point3d(2, 0, 0));
    
                acCirc.TransformBy(Matrix3d.Displacement(acVec3d));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("MoveObject")> _
    Public Sub MoveObject()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle that is at 2,2 with a radius of 0.5
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 0.5
    
                '' Create a matrix and move the circle using a vector from (0,0,0) to (2,0,0)
                Dim acPt3d As Point3d = New Point3d(0, 0, 0)
                Dim acVec3d As Vector3d = acPt3d.GetVectorTo(New Point3d(2, 0, 0))
    
                acCirc.TransformBy(Matrix3d.Displacement(acVec3d))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MoveObject()
        ' Create the circle
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2#: center(1) = 2#: center(2) = 0#
        radius = 0.5
        Set circleObj = ThisDrawing.ModelSpace. _
                                      AddCircle(center, radius)
        ZoomAll
     
        ' Define the points that make up the move vector.
        ' The move vector will move the circle 2 units
        ' along the x axis.
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
        point1(0) = 0: point1(1) = 0: point1(2) = 0
        point2(0) = 2: point2(1) = 0: point2(2) = 0
     
        ' Move the circle
        circleObj.Move point1, point2
        circleObj.Update
    End Sub
