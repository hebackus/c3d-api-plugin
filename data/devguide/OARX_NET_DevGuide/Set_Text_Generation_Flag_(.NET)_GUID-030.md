<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Format Single-Line Text (.NET) > Set Text Generation Flag (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-030E12E4-38EC-4B98-AA24-70665151DB71.htm -->

# Set Text Generation Flag (.NET)

The text generation flag specifies if text is displayed backwards or upside-down. Use the FlagBits property to define if a text style controls the display of text to be displayed backwards or upside-down, or use the IsMirroredInX and IsMirroredInY properties of a text object to control individually control a text object. 

Set FlagBits to 2 if you want text to be displayed backwards and 4 if it should be displayed upside-down. Use a value of 6 to display text both backwards and upside-down. If you are modifying a text object, set IsMirroredInX to TRUE if you want the text to appear backwards and set IsMirroredInY to TRUE if you want it to be displayed upside-down. 

## Display text backwards

The following example creates a single-line text object, then sets it to be displayed backwards using the IsMirroredInX property. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("BackwardsText")]
    public static void BackwardsText()
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
                acText.Position = new Point3d(3, 3, 0);
                acText.Height = 0.5;
                acText.TextString = "Hello, World.";
    
                // Display the text backwards
                acText.IsMirroredInX = true;
    
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
     
    <CommandMethod("BackwardsText")> _
    Public Sub BackwardsText()
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
                acText.Position = New Point3d(3, 3, 0)
                acText.Height = 0.5
                acText.TextString = "Hello, World."
    
                '' Display the text backwards
                acText.IsMirroredInX = True
    
                acBlkTblRec.AppendEntity(acText)
                acTrans.AddNewlyCreatedDBObject(acText, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub BackwardsText()
        Dim textObj As AcadText
        Dim textString As String
        Dim insertionPoint(0 To 2) As Double
        Dim height As Double
     
        ' Create the text object
        textString = "Hello, World."
        insertionPoint(0) = 3
        insertionPoint(1) = 3
        insertionPoint(2) = 0
        height = 0.5
        Set textObj = ThisDrawing.ModelSpace. _
                          AddText(textString, insertionPoint, height)
     
        ' Change the value of the TextGenerationFlag
        textObj.TextGenerationFlag = acTextFlagBackward
        textObj.Update
    End Sub
