<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Offset Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-80D106A9-A16F-4F32-BDE2-5C5B1F7C2C84.htm -->

# Offset Objects (.NET)

Offsetting an object creates a new object at a specified offset distance from the original object. You can offset arcs, circles, ellipses, lines, lightweight polylines, polylines, splines, and xlines. 

To offset an object, use the GetOffsetCurves method provided for that object. The function requires a positive or negative numeric value for the distance to offset the object. If the distance is negative, it is interpreted by AutoCAD as being an offset to make a “smaller” curve (that is, for an arc it would offset to a radius that is the given distance less than the starting curve's radius). If “smaller” has no meaning, then AutoCAD would offset in the direction of smaller _X,Y,Z_ WCS coordinates. 

For many objects, the result of this operation will be a single new curve (which may not be of the same type as the original curve). For example, offsetting an ellipse will result in a spline because the result does fit the equation of an ellipse. In some cases it may be necessary for the offset result to be several curves. Because of this, the function returns a DBObjectCollection object, which contains all the objects that are created by offsetting the curve. The returned DBObjectCollection object needs to be iterated for each object created and then be appended to the drawing database. 

## Offset a polyline

This example creates a lightweight polyline and then offsets it. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("OffsetObject")]
    public static void OffsetObject()
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
                acPoly.AddVertexAt(5, new Point2d(4, 1), 0, 0, 0);
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
    
                // Offset the polyline a given distance
                DBObjectCollection acDbObjColl = acPoly.GetOffsetCurves(0.25);
    
                // Step through the new objects created
                foreach (Entity acEnt in acDbObjColl)
                {
                    // Add each offset object
                    acBlkTblRec.AppendEntity(acEnt);
                    acTrans.AddNewlyCreatedDBObject(acEnt, true);
                }
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("OffsetObject")> _
    Public Sub OffsetObject()
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
                acPoly.AddVertexAt(5, New Point2d(4, 1), 0, 0, 0)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
    
                '' Offset the polyline a given distance
                Dim acDbObjColl As DBObjectCollection = acPoly.GetOffsetCurves(0.25)
    
                '' Step through the new objects created
                For Each acEnt As Entity In acDbObjColl
                    '' Add each offset object
                    acBlkTblRec.AppendEntity(acEnt)
                    acTrans.AddNewlyCreatedDBObject(acEnt, True)
                Next
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub OffsetObject()
        ' Create the polyline
        Dim plineObj As AcadLWPolyline
        Dim points(0 To 11) As Double
        points(0) = 1: points(1) = 1
        points(2) = 1: points(3) = 2
        points(4) = 2: points(5) = 2
        points(6) = 3: points(7) = 2
        points(8) = 4: points(9) = 4
        points(10) = 4: points(11) = 1
        Set plineObj = ThisDrawing.ModelSpace. _
                                        AddLightWeightPolyline(points)
        plineObj.Closed = True
        ZoomAll
     
        ' Offset the polyline
        Dim offsetObj As Variant
        offsetObj = plineObj.Offset(0.25)
     
        ZoomAll
    End Sub
