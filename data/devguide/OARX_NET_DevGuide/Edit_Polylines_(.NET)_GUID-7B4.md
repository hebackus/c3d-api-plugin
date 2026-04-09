<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Edit Polylines (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7B4A7B69-8780-4F8E-A1C6-A195CA1F122E.htm -->

# Edit Polylines (.NET)

2D and 3D polylines, rectangles, polygons, donuts, and 3D polygon meshes are all polyline variants and are edited in the same way. 

AutoCAD recognizes both fit polylines and spline-fit polylines. A spline-fit polyline uses a curve fit, similar to a B-spline. There are two kinds of spline-fit polylines: quadratic and cubic. Both polylines are controlled by the SPLINETYPE system variable. A fit polyline uses standard curves for curve fit and utilizes any tangent directions set on any given vertex. 

To edit a polyline, use the properties and methods of the Polyline, Polyline2d, or Polyline3d object. Use the following properties and methods to open or close a polyline, change the coordinates of a polyline vertex, or add a vertex: 

Closed property
    

Opens or closes the polyline. 

ConstantWidth property
    

Sets the constant width for a lightweight and 2D polyline. 

AppendVertex method
    

Adds a vertex to a 2D or 3D polyline. 

AddVertexAt method
    

Adds a vertex to a lightweight polyline. 

ReverseCurve
    

Reverses the direction of the polyline. 

Use the following methods to update the bulge or width of a polyline: 

SetBulgeAt
    

Sets the bulge of a light polyline, given the segment index. 

SetStartWidthAt
    

Sets the start width of a lightweight polyline, given the segment index. 

Straighten
    

Straightens a 2D or 3D polyline. 

## Edit a polyline

This example creates a lightweight polyline. It then adds a bulge to the third segment of the polyline, appends a vertex to the polyline, changes the width of the last segment, and finally closes the polyline. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("EditPolyline")]
    public static void EditPolyline()
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
                acPoly.AddVertexAt(0, new Point2d(1, 1), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(1, 2), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(2, 2), 0, 0, 0);
                acPoly.AddVertexAt(3, new Point2d(3, 2), 0, 0, 0);
                acPoly.AddVertexAt(4, new Point2d(4, 4), 0, 0, 0);
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
    
                // Sets the bulge at index 3
                acPoly.SetBulgeAt(3, -0.5);
    
                // Add a new vertex
                acPoly.AddVertexAt(5, new Point2d(4, 1), 0, 0, 0);
    
                // Sets the start and end width at index 4
                acPoly.SetStartWidthAt(4, 0.1);
                acPoly.SetEndWidthAt(4, 0.5);
    
                // Close the polyline
                acPoly.Closed = true;
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
     
    <CommandMethod("EditPolyline")> _
    Public Sub EditPolyline()
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
                acPoly.AddVertexAt(0, New Point2d(1, 1), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(1, 2), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(2, 2), 0, 0, 0)
                acPoly.AddVertexAt(3, New Point2d(3, 2), 0, 0, 0)
                acPoly.AddVertexAt(4, New Point2d(4, 4), 0, 0, 0)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
    
                '' Sets the bulge at index 3
                acPoly.SetBulgeAt(3, -0.5)
    
                '' Add a new vertex
                acPoly.AddVertexAt(5, New Point2d(4, 1), 0, 0, 0)
    
                '' Sets the start and end width at index 4
                acPoly.SetStartWidthAt(4, 0.1)
                acPoly.SetEndWidthAt(4, 0.5)
    
                '' Close the polyline
                acPoly.Closed = True
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EditPolyline()
        Dim plineObj As AcadLWPolyline
        Dim points(0 To 9) As Double
     
        ' Define the 2D polyline points
        points(0) = 1: points(1) = 1
        points(2) = 1: points(3) = 2
        points(4) = 2: points(5) = 2
        points(6) = 3: points(7) = 2
        points(8) = 4: points(9) = 4
     
        ' Create a light weight Polyline object
        Set plineObj = ThisDrawing.ModelSpace. _
                                     AddLightWeightPolyline(points)
     
        ' Add a bulge to segment 3
        plineObj.SetBulge 3, -0.5
     
        ' Define the new vertex
        Dim newVertex(0 To 1) As Double
        newVertex(0) = 4: newVertex(1) = 1
     
        ' Add the vertex to the polyline
        plineObj.AddVertex 5, newVertex
     
        ' Set the width of the new segment
        plineObj.SetWidth 4, 0.1, 0.5
     
        ' Close the polyline
        plineObj.Closed = True
        plineObj.Update
    End Sub
