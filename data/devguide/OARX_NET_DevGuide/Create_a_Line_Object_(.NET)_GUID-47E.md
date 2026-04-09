<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Lines (.NET) > Create a Line Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-47E8A12E-2ED4-4E78-ADA3-AAC9B4223C3C.htm -->

# Create a Line Object (.NET)

This example adds a line that starts at (5,5,0) and ends at (12,3,0) to Model space. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddLine")]
    public static void AddLine()
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
    
            // Create a line that starts at 5,5 and ends at 12,3
            using (Line acLine = new Line(new Point3d(5, 5, 0),
                                          new Point3d(12, 3, 0)))
            {
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine);
                acTrans.AddNewlyCreatedDBObject(acLine, true);
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
     
    <CommandMethod("AddLine")> _
    Public Sub AddLine()
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
    
            '' Create a line that starts at 5,5 and ends at 12,3
            Using acLine As Line = New Line(New Point3d(5, 5, 0), _
                                            New Point3d(12, 3, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine)
                acTrans.AddNewlyCreatedDBObject(acLine, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub AddLine()
        ' Define the start point
        Dim ptStr(0 To 2) As Double
        ptStr(0) = 5: ptStr(1) = 5: ptStr(2) = 0#
     
        ' Define the end point
        Dim ptEnd(0 To 2) As Double
        ptEnd(0) = 12: ptEnd(1) = 3: ptEnd(2) = 0#
     
        ' Create a Line object in model space
        Dim lineObj As AcadLine
        Set lineObj = ThisDrawing.ModelSpace.AddLine(ptStr, ptEnd)
     
        ThisDrawing.Application.ZoomAll
    End Sub
