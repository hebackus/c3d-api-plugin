<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Transform Objects (.NET) > Scale Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-50D25B16-2FBF-4E81-B934-A26F699F31BC.htm -->

# Scale Objects (.NET)

You scale an object by specifying a base point and scale factor based on the current drawing units. You can scale all drawing objects, as well as attribute reference objects. 

To scale an object, use the Scaling function of a transformation matrix. This function requires a numeric value for the scale factor of the object and a Point3d object for the base point of the scaling operation. The Scaling function scales the object equally in the _X_ , _Y_ , and _Z_ directions. The dimensions of the object are multiplied by the scale factor. A scale factor greater than 1 enlarges the object. A scale factor between 0 and 1 reduces the object. 

Note: If you need to scale an object non-uniformly, you need to initialize a transformation matrix using the appropriate data array and then use the TransformBy method of the object. 

## Scale a polyline

This example creates a closed lightweight polyline and then scales the polyline by 0.5 from the base point (4,4.25,0). 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("ScaleObject")]
    public static void ScaleObject()
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
    
                // Reduce the object by a factor of 0.5 
                // using a base point of (4,4.25,0)
                acPoly.TransformBy(Matrix3d.Scaling(0.5, new Point3d(4, 4.25, 0)));
    
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
     
    <CommandMethod("ScaleObject")> _
    Public Sub ScaleObject()
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
    
                '' Reduce the object by a factor of 0.5 
                '' using a base point of (4,4.25,0)
                acPoly.TransformBy(Matrix3d.Scaling(0.5, New Point3d(4, 4.25, 0)))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ScaleObject()
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
     
        ' Define the scale
        Dim basePoint(0 To 2) As Double
        Dim scalefactor As Double
        basePoint(0) = 4: basePoint(1) = 4.25: basePoint(2) = 0
        scalefactor = 0.5
     
        ' Scale the polyline
        plineObj.ScaleEntity basePoint, scalefactor
        plineObj.Update
    End Sub
