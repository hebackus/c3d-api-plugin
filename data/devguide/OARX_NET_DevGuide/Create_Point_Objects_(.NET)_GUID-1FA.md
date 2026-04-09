<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Point Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-1FA67D6C-09E2-4051-BE77-08463C1C0072.htm -->

# Create Point Objects (.NET)

Point objects can be useful, for example, as node or reference points that you can snap to and offset objects from. You can set the style of the point and its size relative to the screen or in absolute units. 

The Pdmode and Pdsize properties of the Database object control the appearance of Point objects. A value of 0, 2, 3, and 4 for Pdmode specify a figure to draw through the point. A value of 1 selects nothing to be displayed. 

Adding 32, 64, or 96 to the previous value selects a shape to draw around the point in addition to the figure drawn through it: 

Pdsize controls the size of the point figures, except for when Pdmode is 0 and 1. A 0 setting generates the point at 5 percent of the graphics area height. Setting Pdsize to a positive value specifies an absolute size for the point figures. A negative value is interpreted as a percentage of the viewport size. The size of all points is recalculated when the drawing is regenerated. 

After you change Pdmode and Pdsize, the appearance of existing points changes the next time the drawing is regenerated. 

## Create a Point object and change its appearance

The following example creates a Point object in Model space at the coordinate (5, 5, 0). The Pdmode and Pdsize properties are then updated. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddPointAndSetPointStyle")]
    public static void AddPointAndSetPointStyle()
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
    
            // Create a point at (4, 3, 0) in Model space
            using (DBPoint acPoint = new DBPoint(new Point3d(4, 3, 0)))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoint);
                acTrans.AddNewlyCreatedDBObject(acPoint, true);
            }
    
            // Set the style for all point objects in the drawing
            acCurDb.Pdmode = 34;
            acCurDb.Pdsize = 1;
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddPointAndSetPointStyle")> _
    Public Sub AddPointAndSetPointStyle()
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
    
            '' Create a point at (4, 3, 0) in Model space
            Using acPoint As DBPoint = New DBPoint(New Point3d(4, 3, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoint)
                acTrans.AddNewlyCreatedDBObject(acPoint, True)
            End Using
    
            '' Set the style for all point objects in the drawing
            acCurDb.Pdmode = 34
            acCurDb.Pdsize = 1
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddPointAndSetPointStyle()
        Dim pointObj As AcadPoint
        Dim location(0 To 2) As Double
     
        ' Define the location of the point
        location(0) = 4#: location(1) = 3#: location(2) = 0#
     
        ' Create the point
        Set pointObj = ThisDrawing.ModelSpace.AddPoint(location)
        ThisDrawing.SetVariable "PDMODE", 34
        ThisDrawing.SetVariable "PDSIZE", 1
     
        ZoomAll
    End Sub
