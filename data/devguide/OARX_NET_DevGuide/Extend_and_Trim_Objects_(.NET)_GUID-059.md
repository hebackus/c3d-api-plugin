<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Extend and Trim Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-059D278C-6CFF-4376-9B9D-DFBE23C3A054.htm -->

# Extend and Trim Objects (.NET)

You can change the angle of arcs and you can change the length of lines, open polylines, elliptical arcs, and open splines. The results are similar to both extending and trimming objects. 

You can extend or trim an object by editing its properties. For example, to lengthen a line, simply change the coordinates of the StartPoint or EndPoint properties. To change the angle of an arc, change the StartAngle or EndAngle property of the arc. Once you have altered an object's property or properties, you might need to regenerate the display to see the changes in the drawing window. 

## Lengthen a line

This example creates a line and then changes the endpoint of that line, resulting in a longer line. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("ExtendObject")]
    public static void ExtendObject()
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
    
            // Create a line that starts at (4,4,0) and ends at (7,7,0)
            using (Line acLine = new Line(new Point3d(4, 4, 0),
                                    new Point3d(7, 7, 0)))
            {
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine);
                acTrans.AddNewlyCreatedDBObject(acLine, true);
    
                // Update the display and diaplay a message box
                acDoc.Editor.Regen();
                Application.ShowAlertDialog("Before extend");
    
                // Double the length of the line
                acLine.EndPoint = acLine.EndPoint + acLine.Delta;
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("ExtendObject")> _
    Public Sub ExtendObject()
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
    
            '' Create a line that starts at (4,4,0) and ends at (7,7,0)
            Using acLine As Line = New Line(New Point3d(4, 4, 0), _
                                            New Point3d(7, 7, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine)
                acTrans.AddNewlyCreatedDBObject(acLine, True)
    
                '' Update the display and diaplay a message box
                acDoc.Editor.Regen()
                Application.ShowAlertDialog("Before extend")
    
                '' Double the length of the line
                acLine.EndPoint = acLine.EndPoint + acLine.Delta
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ExtendObject()
        ' Define and create the line
        Dim lineObj As AcadLine
        Dim startPoint(0 To 2) As Double
        Dim endPoint(0 To 2)  As Double
        startPoint(0) = 4
        startPoint(1) = 4
        startPoint(2) = 0
        endPoint(0) = 7
        endPoint(1) = 7
        endPoint(2) = 0
        Set lineObj = ThisDrawing.ModelSpace. _
                                    AddLine(startPoint, endPoint)
        lineObj.Update
     
        ' Double the length of the line
        endPoint(0) = lineObj.endPoint(0) + lineObj.Delta(0)
        endPoint(1) = lineObj.endPoint(1) + lineObj.Delta(1)
        endPoint(2) = lineObj.endPoint(2) + lineObj.Delta(2)
        lineObj.endPoint = endPoint
        lineObj.Update
    End Sub
