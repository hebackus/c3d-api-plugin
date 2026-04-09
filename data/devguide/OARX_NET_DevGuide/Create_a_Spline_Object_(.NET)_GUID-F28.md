<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Curved Objects (.NET) > Create a Spline Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F28F37BA-E004-4948-8336-6D398FED7748.htm -->

# Create a Spline Object (.NET)

This example creates a circle in Model space using three points (0, 0, 0), (5, 5, 0), and (10, 0, 0). The spline has start and end tangents of (0.5, 0.5, 0.0). 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddSpline")]
    public static void AddSpline()
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
    
            // Define the fit points for the spline
            Point3dCollection ptColl = new Point3dCollection();
            ptColl.Add(new Point3d(0, 0, 0));
            ptColl.Add(new Point3d(5, 5, 0));
            ptColl.Add(new Point3d(10, 0, 0));
    
            // Get a 3D vector from the point (0.5,0.5,0)
            Vector3d vecTan = new Point3d(0.5, 0.5, 0).GetAsVector();
    
            // Create a spline through (0, 0, 0), (5, 5, 0), and (10, 0, 0) with a
            // start and end tangency of (0.5, 0.5, 0.0)
            using (Spline acSpline = new Spline(ptColl, vecTan, vecTan, 4, 0.0))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSpline);
                acTrans.AddNewlyCreatedDBObject(acSpline, true);
            }
    
            // Save the new line to the database
            acTrans.Commit();
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddSpline")> _
    Public Sub AddSpline()
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
    
            '' Define the fit points for the spline
            Dim ptColl As Point3dCollection = New Point3dCollection()
            ptColl.Add(New Point3d(0, 0, 0))
            ptColl.Add(New Point3d(5, 5, 0))
            ptColl.Add(New Point3d(10, 0, 0))
    
            '' Get a 3D vector from the point (0.5,0.5,0)
            Dim vecTan As Vector3d = New Point3d(0.5, 0.5, 0).GetAsVector
    
            '' Create a spline through (0, 0, 0), (5, 5, 0), and (10, 0, 0) with a
            '' start and end tangency of (0.5, 0.5, 0.0)
            Using acSpline As Spline = New Spline(ptColl, vecTan, vecTan, 4, 0.0)
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSpline)
                acTrans.AddNewlyCreatedDBObject(acSpline, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub AddSpline()
        ' This example creates a spline object in model space.
        ' Declare the variables needed
        Dim splineObj As AcadSpline
        Dim startTan(0 To 2) As Double
        Dim endTan(0 To 2) As Double
        Dim fitPoints(0 To 8) As Double
     
        ' Define the variables
        startTan(0) = 0.5: startTan(1) = 0.5: startTan(2) = 0
        endTan(0) = 0.5: endTan(1) = 0.5: endTan(2) = 0
        fitPoints(0) = 1: fitPoints(1) = 1: fitPoints(2) = 0
        fitPoints(3) = 5: fitPoints(4) = 5: fitPoints(5) = 0
        fitPoints(6) = 10: fitPoints(7) = 0: fitPoints(8) = 0
     
        ' Create the spline
        Set splineObj = ThisDrawing.ModelSpace.AddSpline _
                            (fitPoints, startTan, endTan)
        ZoomAll
    End Sub
