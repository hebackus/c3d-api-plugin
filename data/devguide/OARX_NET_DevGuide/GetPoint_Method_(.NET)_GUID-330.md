<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Prompt for User Input (.NET) > GetPoint Method (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-33058D80-EA6B-4A19-9F07-F20BC5EBC530.htm -->

# GetPoint Method (.NET)

The GetPoint method prompts the user to specify a point at the Command prompt. The PromptPointOptions object allows you to control the input entered and how the prompt message appears. The UseBasePoint and BasePoint properties of the PromptPointOptions object controls if a rubber-band line is drawn from a base point. The Keywords property of the PromptPointOptions object allows you to define keywords that can be entered at the Command prompt in addition to specifying a point. 

## Get a point selected by the user

The following example prompts the user for two points, then draws a line using those points as the start point and endpoint. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetPointsFromUser")]
    public static void GetPointsFromUser()
    {
        // Get the current database and start the Transaction Manager
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        PromptPointResult pPtRes;
        PromptPointOptions pPtOpts = new PromptPointOptions("");
    
        // Prompt for the start point
        pPtOpts.Message = "\nEnter the start point of the line: ";
        pPtRes = acDoc.Editor.GetPoint(pPtOpts);
        Point3d ptStart = pPtRes.Value;
    
        // Exit if the user presses ESC or cancels the command
        if (pPtRes.Status == PromptStatus.Cancel) return;
    
        // Prompt for the end point
        pPtOpts.Message = "\nEnter the end point of the line: ";
        pPtOpts.UseBasePoint = true;
        pPtOpts.BasePoint = ptStart;
        pPtRes = acDoc.Editor.GetPoint(pPtOpts);
        Point3d ptEnd = pPtRes.Value;
    
        if (pPtRes.Status == PromptStatus.Cancel) return;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            BlockTable acBlkTbl;
            BlockTableRecord acBlkTblRec;
    
            // Open Model space for write
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                            OpenMode.ForRead) as BlockTable;
    
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Define the new line
            using (Line acLine = new Line(ptStart, ptEnd))
            {
                // Add the line to the drawing
                acBlkTblRec.AppendEntity(acLine);
                acTrans.AddNewlyCreatedDBObject(acLine, true);
            }
    
            // Zoom to the extents or limits of the drawing
            acDoc.SendStringToExecute("._zoom _all ", true, false, false);
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("GetPointsFromUser")> _
    Public Sub GetPointsFromUser()
        '' Get the current database and start the Transaction Manager
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Dim pPtRes As PromptPointResult
        Dim pPtOpts As PromptPointOptions = New PromptPointOptions("")
    
        '' Prompt for the start point
        pPtOpts.Message = vbLf & "Enter the start point of the line: "
        pPtRes = acDoc.Editor.GetPoint(pPtOpts)
        Dim ptStart As Point3d = pPtRes.Value
    
        '' Exit if the user presses ESC or cancels the command
        If pPtRes.Status = PromptStatus.Cancel Then Exit Sub
    
        '' Prompt for the end point
        pPtOpts.Message = vbLf & "Enter the end point of the line: "
        pPtOpts.UseBasePoint = True
        pPtOpts.BasePoint = ptStart
        pPtRes = acDoc.Editor.GetPoint(pPtOpts)
        Dim ptEnd As Point3d = pPtRes.Value
    
        If pPtRes.Status = PromptStatus.Cancel Then Exit Sub
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            Dim acBlkTbl As BlockTable
            Dim acBlkTblRec As BlockTableRecord
    
            '' Open Model space for write
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Define the new line
            Using acLine As Line = New Line(ptStart, ptEnd)
                '' Add the line to the drawing
                acBlkTblRec.AppendEntity(acLine)
                acTrans.AddNewlyCreatedDBObject(acLine, True)
            End Using
    
            '' Zoom to the extents or limits of the drawing
            acDoc.SendStringToExecute("._zoom _all ", True, False, False)
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetPointsFromUser()
        Dim startPnt As Variant
        Dim endPnt As Variant
        Dim prompt1 As String
        Dim prompt2 As String
     
        prompt1 = vbCrLf & "Enter the start point of the line: "
        prompt2 = vbCrLf & "Enter the end point of the line: "
     
        ' Get the first point without entering a base point
        startPnt = ThisDrawing.Utility.GetPoint(, prompt1)
     
        ' Use the point entered above as the base point
        endPnt = ThisDrawing.Utility.GetPoint(startPnt, prompt2)
     
        ' Create a line using the two points entered
        ThisDrawing.ModelSpace.AddLine startPnt, endPnt
        ThisDrawing.Application.ZoomAll
    End Sub
