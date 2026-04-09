<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Curved Objects (.NET) > Create an Arc Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-EF4D9742-F41F-48E1-BDDC-235069C52176.htm -->

# Create an Arc Object (.NET)

This example creates an arc in Model space with a center point of (6.25,9.125,0), a radius of 6, start angle of 1.117 (64 degrees), and an end angle of 3.5605 (204 degrees). 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddArc")]
    public static void AddArc()
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
    
            // Create an arc that is at 6.25,9.125 with a radius of 6, and
            // starts at 64 degrees and ends at 204 degrees
            using (Arc acArc = new Arc(new Point3d(6.25, 9.125, 0),
                                6, 1.117, 3.5605))
            {
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acArc);
                acTrans.AddNewlyCreatedDBObject(acArc, true);
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
     
    <CommandMethod("AddArc")> _
    Public Sub AddArc()
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
    
            '' Create an arc that is at 6.25,9.125 with a radius of 6, and
            '' starts at 64 degrees and ends at 204 degrees
            Using acArc As Arc = New Arc(New Point3d(6.25, 9.125, 0), _
                                         6, 1.117, 3.5605)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acArc)
                acTrans.AddNewlyCreatedDBObject(acArc, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub AddArc()
        ' Define the center point
        Dim ptCen(0 To 2) As Double
        ptCen(0) = 6.25: ptCen(1) = 9.125: ptCen(2) = 0#
     
        ' Create an Arc object in model space
        Dim arcObj As AcadArc
        Set arcObj = ThisDrawing.ModelSpace.AddArc(ptCen, 6#, 1.117, 3.5605)
     
        ThisDrawing.Application.ZoomAll
    End Sub
