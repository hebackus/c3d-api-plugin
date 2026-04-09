<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Transform Objects (.NET) > Rotate Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DAF76951-DD0C-413F-86A8-471E2B94C1C0.htm -->

# Rotate Objects (.NET)

You can rotate all drawing objects and attribute reference objects. 

To rotate an object, use the Rotation function of a transformation matrix. This function requires a rotation angle represented in radians, an axis of rotation, and a base point. The axis of rotation must be expressed as a Vector3d object and the base point as a Point3d object. This angle determines how far an object rotates around the base point relative to its current location. 

## Rotate a polyline about a base point

This example creates a closed lightweight polyline, and then rotates the polyline 45 degrees about the base point (4, 4.25, 0). 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("RotateObject")]
    public static void RotateObject()
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
    
            // Create a lightweight polyline
            using (Polyline acPoly = new Polyline())
            {
                acPoly.AddVertexAt(0, new Point2d(1, 2), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(1, 3), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(2, 3), 0, 0, 0);
                acPoly.AddVertexAt(3, new Point2d(3, 3), 0, 0, 0);
                acPoly.AddVertexAt(4, new Point2d(4, 4), 0, 0, 0);
                acPoly.AddVertexAt(5, new Point2d(4, 2), 0, 0, 0);
    
                // Close the polyline
                acPoly.Closed = true;
    
                Matrix3d curUCSMatrix = acDoc.Editor.CurrentUserCoordinateSystem;
                CoordinateSystem3d curUCS = curUCSMatrix.CoordinateSystem3d;
    
                // Rotate the polyline 45 degrees, around the Z-axis of the current UCS
                // using a base point of (4,4.25,0)
                acPoly.TransformBy(Matrix3d.Rotation(0.7854,
                                                     curUCS.Zaxis,
                                                     new Point3d(4, 4.25, 0)));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
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
     
    <CommandMethod("RotateObject")> _
    Public Sub RotateObject()
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
    
            '' Create a lightweight polyline
            Using acPoly As Polyline = New Polyline()
                acPoly.AddVertexAt(0, New Point2d(1, 2), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(1, 3), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(2, 3), 0, 0, 0)
                acPoly.AddVertexAt(3, New Point2d(3, 3), 0, 0, 0)
                acPoly.AddVertexAt(4, New Point2d(4, 4), 0, 0, 0)
                acPoly.AddVertexAt(5, New Point2d(4, 2), 0, 0, 0)
    
                '' Close the polyline
                acPoly.Closed = True
    
                Dim curUCSMatrix As Matrix3d = acDoc.Editor.CurrentUserCoordinateSystem
                Dim curUCS As CoordinateSystem3d = curUCSMatrix.CoordinateSystem3d
    
                '' Rotate the polyline 45 degrees, around the Z-axis of the current UCS
                '' using a base point of (4,4.25,0)
                acPoly.TransformBy(Matrix3d.Rotation(0.7854, _
                                                     curUCS.Zaxis, _
                                                     New Point3d(4, 4.25, 0)))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub RotateObject()
        ' Create the polyline
        Dim plineObj As AcadLWPolyline
        Dim points(0 To 11) As Double
        points(0) = 1: points(1) = 2
        points(2) = 1: points(3) = 3
        points(4) = 2: points(5) = 3
        points(6) = 3: points(7) = 3
        points(8) = 4: points(9) = 4
        points(10) = 4: points(11) = 2
        Set plineObj = ThisDrawing.ModelSpace. _
                                        AddLightWeightPolyline(points)
        plineObj.Closed = True
        ZoomAll
     
        ' Define the rotation of 45 degrees about a
        ' base point of (4, 4.25, 0)
        Dim basePoint(0 To 2) As Double
        Dim rotationAngle As Double
        basePoint(0) = 4: basePoint(1) = 4.25: basePoint(2) = 0
        rotationAngle = 0.7853981   ' 45 degrees
     
        ' Rotate the polyline
        plineObj.Rotate basePoint, rotationAngle
        plineObj.Update
    End Sub
