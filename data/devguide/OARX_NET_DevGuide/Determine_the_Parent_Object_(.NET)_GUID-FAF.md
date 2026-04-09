<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Determine the Parent Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FAFA37D8-1C15-408B-8419-DB27225664B6.htm -->

# Determine the Parent Object (.NET)

Graphical objects are appended to a BlockTableRecord object, such as Model or Paper space. You reference the blocks that represent Model and Paper space through the BlockTable object. If you want to work in the current space instead of a specific space, you get the ObjectId for the current space from the current database with the CurrentSpaceId property. 

The ObjectId for the block table records of Model and Paper space can be retrieved from the BlockTable object using a property or the GetBlockModelSpaceId and GetBlockPaperSpaceId methods of the SymbolUtilityServices class under the DatabaseServices namespace. 

## Access Model space, Paper space or the current space

The following example demonstrates how to access the block table records associated with Model space, Paper space or the current space. Once the block table record is referenced, a new line is added to the block table record. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("AccessSpace")]
    public static void AccessSpace()
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
    
            // Open the Block table record for read
            BlockTableRecord acBlkTblRec;
    
            // Request which table record to open
            PromptKeywordOptions pKeyOpts = new PromptKeywordOptions("");
            pKeyOpts.Message = "\nEnter which space to create the line in ";
            pKeyOpts.Keywords.Add("Model");
            pKeyOpts.Keywords.Add("Paper");
            pKeyOpts.Keywords.Add("Current");
            pKeyOpts.AllowNone = false;
            pKeyOpts.AppendKeywordsToMessage = true;
    
            PromptResult pKeyRes = acDoc.Editor.GetKeywords(pKeyOpts);
    
            if (pKeyRes.StringResult == "Model")
            {
                // Get the ObjectID for Model space from the Block table
                acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                                OpenMode.ForWrite) as BlockTableRecord;
            }
            else if (pKeyRes.StringResult == "Paper")
            {
                // Get the ObjectID for Paper space from the Block table
                acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                                OpenMode.ForWrite) as BlockTableRecord;
            }
            else
            {
                // Get the ObjectID for the current space from the database
                acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId,
                                                OpenMode.ForWrite) as BlockTableRecord;
            }
    
            // Create a line that starts at 2,5 and ends at 10,7
            using (Line acLine = new Line(new Point3d(2, 5, 0),
                                    new Point3d(10, 7, 0)))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine);
                acTrans.AddNewlyCreatedDBObject(acLine, true);
            }
    
            // Save the new line to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("AccessSpace")> _
    Public Sub AccessSpace()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record for read
            Dim acBlkTblRec As BlockTableRecord
    
            '' Request which table record to open
            Dim pKeyOpts As PromptKeywordOptions = New PromptKeywordOptions("")
            pKeyOpts.Message = vbLf & "Enter which space to create the line in "
            pKeyOpts.Keywords.Add("Model")
            pKeyOpts.Keywords.Add("Paper")
            pKeyOpts.Keywords.Add("Current")
            pKeyOpts.AllowNone = False
            pKeyOpts.AppendKeywordsToMessage = True
    
            Dim pKeyRes As PromptResult = acDoc.Editor.GetKeywords(pKeyOpts)
    
            If pKeyRes.StringResult = "Model" Then
                '' Get the ObjectID for Model space from the Block table
                acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                                OpenMode.ForWrite)
            ElseIf pKeyRes.StringResult = "Paper" Then
                '' Get the ObjectID for Paper space from the Block table
                acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace), _
                                                OpenMode.ForWrite)
            Else
                '' Get the ObjectID for the current space from the database
                acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, _
                                                OpenMode.ForWrite)
            End If
    
            '' Create a line that starts at 2,5 and ends at 10,7
            Using acLine As Line = New Line(New Point3d(2, 5, 0), _
                                            New Point3d(10, 7, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine)
                acTrans.AddNewlyCreatedDBObject(acLine, True)
            End Using
    
            '' Save the new line to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public Sub AccessSpace()
        ' Define the valid keywords
        Dim keywordList As String
        keywordList = "Model Paper Current"
     
        ' Call InitializeUserInput to setup the keywords
        ThisDrawing.Utility.InitializeUserInput 1, keywordList
     
        ' Get the user input
        Dim retVal As Variant
        retVal = ThisDrawing.Utility.GetKeyword(vbLf & _
                                       "Enter which space to create the line in " & _
                                       "[Model/Paper/Current]: ")
     
        ' Get the entered keyword
        Dim strVal As String
        strVal = ThisDrawing.Utility.GetInput
     
        Dim acSpaceObj As Object
     
        If strVal = "Model" Or _
          (strVal = "Current" And ThisDrawing.ActiveSpace = acModelSpace) Then
            '' Get the Model space object
            Set acSpaceObj = ThisDrawing.ModelSpace
        Else
            '' Get the Paper space object
            Set acSpaceObj = ThisDrawing.PaperSpace
        End If
     
        '' Create a line that starts at 2,5 and ends at 10,7
        Dim acLine As AcadLine
        Dim dPtStr(0 To 2) As Double
        dPtStr(0) = 2: dPtStr(1) = 5: dPtStr(2) = 0#
     
        Dim dPtEnd(0 To 2) As Double
        dPtEnd(0) = 10: dPtEnd(1) = 7: dPtEnd(2) = 0#
     
        Set acLine = acSpaceObj.AddLine(dPtStr, dPtEnd)
    End Sub
