<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Multiline Text (.NET) > Create Multiline Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3AD06F39-898D-48A1-8E09-E2754BE6765B.htm -->

# Create Multiline Text (.NET)

You can create a multiline text object by first creating an instance of a MText object and then adding it to a block table record that represents Model or Paper space. The MText object constructor does not take any parameters. After an instance of an MText object is created, you can then assign it a text string, insertion point, and width among other values using its properties. Other properties that you can change affect the object’s text height, justification, rotation angle, and text style, or apply character formatting to selected characters 

## Create a multiline text object

The following example creates an MText object in Model space, at the coordinate (2, 2, 0). 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateMText")]
    public static void CreateMText()
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
    
            // Create a multiline text object
            using (MText acMText = new MText())
            {
                acMText.Location = new Point3d(2, 2, 0);
                acMText.Width = 4;
                acMText.Contents = "This is a text string for the MText object.";
    
                acBlkTblRec.AppendEntity(acMText);
                acTrans.AddNewlyCreatedDBObject(acMText, true);
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
     
    <CommandMethod("CreateMText")> _
    Public Sub CreateMText()
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
    
            '' Create a multiline text object
            Using acMText As MText = New MText()
                acMText.Location = New Point3d(2, 2, 0)
                acMText.Width = 4
                acMText.Contents = "This is a text string for the MText object."
    
                acBlkTblRec.AppendEntity(acMText)
                acTrans.AddNewlyCreatedDBObject(acMText, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateMText()
        Dim mtextObj As AcadMText
        Dim insertPoint(0 To 2) As Double
        Dim width As Double
        Dim textString As String
     
        insertPoint(0) = 2
        insertPoint(1) = 2
        insertPoint(2) = 0
        width = 4
        textString = "This is a text string for the mtext object."
     
        ' Create a text Object in model space
        Set mtextObj = ThisDrawing.ModelSpace. _
                           AddMText(insertPoint, width, textString)
        ZoomAll
    End Sub
