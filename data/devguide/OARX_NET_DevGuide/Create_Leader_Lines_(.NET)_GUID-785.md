<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Leaders and Annotation (.NET) > Create Leader Lines (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-785296F3-C81C-41D3-950E-43DF70BDD503.htm -->

# Create Leader Lines (.NET)

You can create a leader line from any point or feature in a drawing and control its appearance. Leaders can be straight line segments or smooth spline curves. Leader color is controlled by the current dimension line color. Leader scale is controlled by the overall dimension scale set in the active dimension style. The type and size of the arrowhead, if one is present, is controlled by the arrowhead defined in the active style. 

A small line known as a hook line usually connects the annotation to the leader. Hook lines appear with multiline text and feature control frames if the last leader line segment is at an angle greater than 15 degrees from horizontal. The hook line is the length of a single arrowhead. If the leader has no annotation, it has no hook line. 

You create a leader by creating an instance of a Leader object. When you create an instance of a Leader object, its constructor does not accept any parameters. The AppendVertex method is used to define the position and length of the leader created. 

## Create a leader line

This example creates a leader line in model space. There is no annotation associated with the leader line. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateLeader")]
    public static void CreateLeader()
    {
        // Get the current database
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
    
            // Create the leader
            using (Leader acLdr = new Leader())
            {
                acLdr.AppendVertex(new Point3d(0, 0, 0));
                acLdr.AppendVertex(new Point3d(4, 4, 0));
                acLdr.AppendVertex(new Point3d(4, 5, 0));
                acLdr.HasArrowHead = true;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acLdr);
                acTrans.AddNewlyCreatedDBObject(acLdr, true);
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreateLeader")> _
    Public Sub CreateLeader()
        '' Get the current database
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
    
            '' Create the leader
            Using acLdr As Leader = New Leader()
                acLdr.AppendVertex(New Point3d(0, 0, 0))
                acLdr.AppendVertex(New Point3d(4, 4, 0))
                acLdr.AppendVertex(New Point3d(4, 5, 0))
                acLdr.HasArrowHead = True
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acLdr)
                acTrans.AddNewlyCreatedDBObject(acLdr, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateLeader()
        Dim leaderObj As AcadLeader
        Dim points(0 To 8) As Double
        Dim leaderType As Integer
        Dim annotationObject As AcadObject
     
        points(0) = 0: points(1) = 0: points(2) = 0
        points(3) = 4: points(4) = 4: points(5) = 0
        points(6) = 4: points(7) = 5: points(8) = 0
        leaderType = acLineWithArrow
        Set annotationObject = Nothing
     
        ' Create the leader object in model space
        Set leaderObj = ThisDrawing.ModelSpace. _
                            AddLeader(points, annotationObject, leaderType)
     
        ZoomAll
    End Sub
