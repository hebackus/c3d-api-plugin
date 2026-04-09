<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Lines (.NET) > Create a Polyline Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-EC036F5A-1F02-40D3-B348-4193BA58CF0C.htm -->

# Create a Polyline Object (.NET)

This example adds a lightweight polyline with two straight segments using the 2D coordinates (2,4), (4,2), and (6,4) to Model space. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddLightweightPolyline")]
    public static void AddLightweightPolyline()
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
    
            // Create a polyline with two segments (3 points)
            using (Polyline acPoly = new Polyline())
            {
                acPoly.AddVertexAt(0, new Point2d(2, 4), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(4, 2), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(6, 4), 0, 0, 0);
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddLightweightPolyline")> _
    Public Sub AddLightweightPolyline()
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
    
            '' Create a polyline with two segments (3 points)
            Using acPoly As Polyline = New Polyline()
                acPoly.AddVertexAt(0, New Point2d(2, 4), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(4, 2), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(6, 4), 0, 0, 0)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub AddLightWeightPolyline()
        Dim plineObj As AcadLWPolyline
        Dim points(0 To 5) As Double
     
        ' Define the 2D polyline points
        points(0) = 2: points(1) = 4
        points(2) = 4: points(3) = 2
        points(4) = 6: points(5) = 4
     
        ' Create a light weight Polyline object in model space
        Set plineObj = ThisDrawing.ModelSpace. _
                       AddLightWeightPolyline(points)
        ThisDrawing.Application.ZoomAll
    End Sub
