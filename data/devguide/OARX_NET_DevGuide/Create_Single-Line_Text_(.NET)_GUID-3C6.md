<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Create Single-Line Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3C694C6C-8BB7-4997-9D1E-1D0B6E810245.htm -->

# Create Single-Line Text (.NET)

Each individual line of text is a distinct object when using single-line text. To create a single-line text object, you create an instance of a DBText object and then add it to either the block table record that represents Model or Paper space. When you create a new instance of a DBText object, you do not pass the constructor any parameters. 

## To Create Line Text

The following example creates a single-line text object in Model space at the coordinate (2, 2, 0) with a height of 0.5 and the text string "Hello, World.". 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateText")]
    public static void CreateText()
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
    
            // Create a single-line text object
            using (DBText acText = new DBText())
            {
                acText.Position = new Point3d(2, 2, 0);
                acText.Height = 0.5;
                acText.TextString = "Hello, World.";
    
                acBlkTblRec.AppendEntity(acText);
                acTrans.AddNewlyCreatedDBObject(acText, true);
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreateText")> _
    Public Sub CreateText()
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
    
            '' Create a single-line text object
            Using acText As DBText = New DBText()
                acText.Position = New Point3d(2, 2, 0)
                acText.Height = 0.5
                acText.TextString = "Hello, World."
    
                acBlkTblRec.AppendEntity(acText)
                acTrans.AddNewlyCreatedDBObject(acText, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateText()
        Dim textObj As AcadText
        Dim textString As String
        Dim insertionPoint(0 To 2) As Double
        Dim height As Double
     
        ' Create the text object
        textString = "Hello, World."
        insertionPoint(0) = 2
        insertionPoint(1) = 2
        insertionPoint(2) = 0
        height = 0.5
     
        Set textObj = ThisDrawing.ModelSpace. _
                          AddText(textString, insertionPoint, height)
        textObj.Update
    End Sub
