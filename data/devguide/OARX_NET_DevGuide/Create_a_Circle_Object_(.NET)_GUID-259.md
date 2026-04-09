<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Curved Objects (.NET) > Create a Circle Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-25923EE3-1C93-4A1E-9A02-5EB4EAF5109F.htm -->

# Create a Circle Object (.NET)

This example creates a circle in Model space with a center point of (2,3,0) and a radius of 4.25. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddCircle")]
    public static void AddCircle()
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
     
    <CommandMethod("AddCircle")> _
    Public Sub AddCircle()
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
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub AddCircle()
        ' Define the center point
        Dim ptCen(0 To 2) As Double
        ptCen(0) = 2: ptCen(1) = 3: ptCen(2) = 0#
     
        ' Create a Circle object in model space
        Dim circObj As AcadCircle
        Set circObj = ThisDrawing.ModelSpace.AddCircle(ptCen, 4.25)
     
        ThisDrawing.Application.ZoomAll
    End Sub
