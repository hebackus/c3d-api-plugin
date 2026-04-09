<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Multiline Text (.NET) > Format Multiline Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-ECEEF65E-C327-44B8-AFB9-C0ACA2CAEF55.htm -->

# Format Multiline Text (.NET)

Newly created multiline text automatically assumes the characteristics of the current text style. The default text style is STANDARD. You can override the default text style by applying formatting to individual characters and applying properties to the multiline text object. You also can indicate formatting or special characters using the methods described in this section. 

Orientation options such as style, justification, width, and rotation affect all text within the multiline text boundary, not specific words or characters. Use the Attachment property to change the justification of a multiline text object, and the Rotation property to control the angle of rotation. 

The TextStyleId property sets the font and formatting characteristics for a multiline text object. As you create multiline text, you can select which style you want to use from a list of existing styles. When you change the style of a multiline text object that has character formatting applied to any portion of the text, the style is applied to the entire object, and some formatting of characters might not be retained. For instance, changing from a TrueType style to a style using an SHX font or to another TrueType font causes the multiline text to use the new font for the entire object, and any character formatting is lost. 

Formatting options such as underlining, stacked text, or fonts can be applied to individual words or characters within a paragraph. You also can change color, font, and text height. You can change the spaces between text characters or increase the width of the characters. 

Use curly braces ({ }) to apply a format change only to the text within the braces. You can nest braces up to eight levels deep. 

You also can enter the ASCII equivalent for control codes within lines or paragraphs to indicate formatting or special characters, such as tolerance or dimensioning symbols. 

The following control characters can be used to create the text in the illustration. (For the ASCII equivalent of this string see the example following the illustration.) 

{{\H1.5x; Big text} \A2; over text\A1;/\A0; under text} 

## Use control characters to format text

The following example creates and formats a multiline text object. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("FormatMText")]
    public static void FormatMText()
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
                acMText.Width = 4.5;
                acMText.Contents = "{{\\H1.5x; Big text}\\A2; over text\\A1;/\\A0;under text}";
    
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
     
    <CommandMethod("FormatMText")> _
    Public Sub FormatMText()
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
                acMText.Width = 4.5
                acMText.Contents = "{{\H1.5x; Big text}\A2; over text\A1;/\A0;under text}"
    
                acBlkTblRec.AppendEntity(acMText)
                acTrans.AddNewlyCreatedDBObject(acMText, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FormatMText()
        Dim mtextObj As AcadMText
        Dim insertPoint(0 To 2) As Double
        Dim width As Double
        Dim textString As String
     
        insertPoint(0) = 2
        insertPoint(1) = 2
        insertPoint(2) = 0
        width = 4.5
     
        ' Define the ASCII characters for the control characters
        Dim OB As Long  ' Open Bracket  {
        Dim CB As Long  ' Close Bracket }
        Dim BS As Long  ' Back Slash    \
        Dim FS As Long  ' Forward Slash /
        Dim SC As Long  ' Semicolon     ;
        OB = Asc("{")
        CB = Asc("}")
        BS = Asc("\")
        FS = Asc("/")
        SC = Asc(";")
     
        ' Assign the text string the following line of control
        ' characters and text characters:
        ' {{\H1.5x; Big text}\A2; over text\A1;/\A0;under text}
     
        textString = Chr(OB) + Chr(OB) + Chr(BS) + "H1.5x" _
        + Chr(SC) + "Big text" + Chr(CB) + Chr(BS) + "A2" _
        + Chr(SC) + "over text" + Chr(BS) + "A1" + Chr(SC) _
        + Chr(FS) + Chr(BS) + "A0" + Chr(SC) + "under text" _
        + Chr(CB)
     
        ' Create a text Object in model space
        Set mtextObj = ThisDrawing.ModelSpace. _
                           AddMText(insertPoint, width, textString)
        ZoomAll
    End Sub
