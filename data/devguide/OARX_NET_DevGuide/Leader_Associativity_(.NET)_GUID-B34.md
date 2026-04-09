<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Leaders and Annotation (.NET) > Leader Associativity (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B34CC3FB-E1B8-434D-AA08-358FEA1935FE.htm -->

# Leader Associativity (.NET)

Leaders are associated with their annotation so that when the annotation moves, the endpoint of the leader moves with it. As you move text and feature control frame annotation, the final leader line segment alternates between attaching to the left side and to the right side of the annotation according to the relation of the annotation to the penultimate (second to last) point of the leader. If the midpoint of the annotation is to the right of the penultimate leader point, then the leader attaches to the right; otherwise, it attaches to the left. 

Removing either object from the drawing using either the Erase, Add (to add a block), or WBlock method will break associativity. If the leader and its annotation are copied together in a single operation, the new copy is associative. If they are copied separately, they will non-associative. If associativity is broken for any reason, for example, by copying only the Leader object or by erasing the annotation, the hook line will be removed from the leader. 

## Associate a leader to the annotation

This example creates an MText object. A leader line is then created using the MText object as its annotation. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddLeaderAnnotation")]
    public static void AddLeaderAnnotation()
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
    
            // Create the MText annotation
            using (MText acMText = new MText())
            {
                acMText.Contents = "Hello, World.";
                acMText.Location = new Point3d(5, 5, 0);
                acMText.Width = 2;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acMText);
                acTrans.AddNewlyCreatedDBObject(acMText, true);
    
                // Create the leader with annotation
                using (Leader acLdr = new Leader())
                {
                    acLdr.AppendVertex(new Point3d(0, 0, 0));
                    acLdr.AppendVertex(new Point3d(4, 4, 0));
                    acLdr.AppendVertex(new Point3d(4, 5, 0));
                    acLdr.HasArrowHead = true;
    
                    // Add the new object to Model space and the transaction
                    acBlkTblRec.AppendEntity(acLdr);
                    acTrans.AddNewlyCreatedDBObject(acLdr, true);
    
                    // Attach the annotation after the leader object is added
                    acLdr.Annotation = acMText.ObjectId;
                    acLdr.EvaluateLeader();
                }
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
     
    <CommandMethod("AddLeaderAnnotation")> _
    Public Sub AddLeaderAnnotation()
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
    
            '' Create the MText annotation
            Using acMText As MText = New MText()
                acMText.Contents = "Hello, World."
                acMText.Location = New Point3d(5, 5, 0)
                acMText.Width = 2
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acMText)
                acTrans.AddNewlyCreatedDBObject(acMText, True)
    
                '' Create the leader with annotation
                Using acLdr As Leader = New Leader()
                    acLdr.AppendVertex(New Point3d(0, 0, 0))
                    acLdr.AppendVertex(New Point3d(4, 4, 0))
                    acLdr.AppendVertex(New Point3d(4, 5, 0))
                    acLdr.HasArrowHead = True
    
                    '' Add the new object to Model space and the transaction
                    acBlkTblRec.AppendEntity(acLdr)
                    acTrans.AddNewlyCreatedDBObject(acLdr, True)
    
                    '' Attach the annotation after the leader object is added
                    acLdr.Annotation = acMText.ObjectId
                    acLdr.EvaluateLeader()
                End Using
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddLeaderAnnotation()
        Dim leaderObj As AcadLeader
        Dim mtextObj As AcadMText
        Dim points(0 To 8) As Double
        Dim insertionPoint(0 To 2) As Double
        Dim width As Double
        Dim leaderType As Integer
        Dim annotationObject As Object
        Dim textString As String, msg As String
     
        ' Create the MText object in model space
        textString = "Hello, World."
        insertionPoint(0) = 5
        insertionPoint(1) = 5
        insertionPoint(2) = 0
        width = 2
        Set mtextObj = ThisDrawing.ModelSpace. _
                           AddMText(insertionPoint, width, textString)
     
        ' Data for Leader
        points(0) = 0: points(1) = 0: points(2) = 0
        points(3) = 4: points(4) = 4: points(5) = 0
        points(6) = 4: points(7) = 5: points(8) = 0
        leaderType = acLineWithArrow
     
        ' Create the Leader object in model space and associate
        ' the MText object with the leader
        Set annotationObject = mtextObj
        Set leaderObj = ThisDrawing.ModelSpace. _
                            AddLeader(points, annotationObject, leaderType)
     
        ZoomAll
    End Sub
