<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Work With Text Styles (.NET) > Assign Fonts (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F3013EB5-214C-415A-B1B9-439C325049FF.htm -->

# Assign Fonts (.NET)

Fonts define the shapes of the text characters that make up each character set. A single font can be used by more than one style. Use the FileName property to set the font file for the text style. You can assign TrueType or AutoCAD-compiled SHX fonts to a text style. 

## Set text fonts

The following example gets the current font values using the Font property for the active text style and then changes the typeface for the font to “PlayBill.” To see the effects of changing the typeface, add some multiline or single-line text to your current drawing before running the example. Note that, if you don't have the PlayBill font on your system, you need to substitute a font you do have in order for this example to work. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("UpdateTextFont")]
    public static void UpdateTextFont()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
     
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the current text style for write
            TextStyleTableRecord acTextStyleTblRec;
            acTextStyleTblRec = acTrans.GetObject(acCurDb.Textstyle,
                                                  OpenMode.ForWrite) as TextStyleTableRecord;
     
            // Get the current font settings
            Autodesk.AutoCAD.GraphicsInterface.FontDescriptor acFont;
            acFont = acTextStyleTblRec.Font;
     
            // Update the text style's typeface with "PlayBill"
            Autodesk.AutoCAD.GraphicsInterface.FontDescriptor acNewFont;
            acNewFont = new
              Autodesk.AutoCAD.GraphicsInterface.FontDescriptor("PlayBill",
                                                                acFont.Bold,
                                                                acFont.Italic,
                                                                acFont.CharacterSet,
                                                                acFont.PitchAndFamily);
     
            acTextStyleTblRec.Font = acNewFont;
     
            acDoc.Editor.Regen();
     
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("UpdateTextFont")> _
    Public Sub UpdateTextFont()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
     
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
            '' Open the current text style for write
            Dim acTextStyleTblRec As TextStyleTableRecord
            acTextStyleTblRec = acTrans.GetObject(acCurDb.Textstyle, _
                                                  OpenMode.ForWrite)
     
            '' Get the current font settings
            Dim acFont As Autodesk.AutoCAD.GraphicsInterface.FontDescriptor
            acFont = acTextStyleTblRec.Font
     
            '' Update the text style's typeface with "PlayBill"
            Dim acNewFont As Autodesk.AutoCAD.GraphicsInterface.FontDescriptor
            acNewFont = New  _
              Autodesk.AutoCAD.GraphicsInterface.FontDescriptor("PlayBill", _
                                                                acFont.Bold, _
                                                                acFont.Italic, _
                                                                acFont.CharacterSet, _
                                                                acFont.PitchAndFamily)
     
            acTextStyleTblRec.Font = acNewFont
     
            acDoc.Editor.Regen()
     
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub UpdateTextFont()
     
        MsgBox "Look at the text now..."
     
        Dim typeFace As String
        Dim SavetypeFace As String
        Dim Bold As Boolean
        Dim Italic As Boolean
        Dim charSet As Long
        Dim PitchandFamily As Long
     
        ' Get the current settings to fill in the
        ' default values for the SetFont method
        ThisDrawing.ActiveTextStyle.GetFont typeFace, _
                      Bold, Italic, charSet, PitchandFamily
     
        ' Change the typeface for the font
        SavetypeFace = typeFace
        typeFace = "PlayBill"
        ThisDrawing.ActiveTextStyle.SetFont typeFace, _
                      Bold, Italic, charSet, PitchandFamily
        ThisDrawing.Regen acActiveViewport
    End Sub
