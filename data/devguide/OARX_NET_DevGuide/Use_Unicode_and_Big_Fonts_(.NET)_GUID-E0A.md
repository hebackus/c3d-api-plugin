<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Work With Text Styles (.NET) > Use Unicode and Big Fonts (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E0A705AF-6357-4F9F-A5E3-EDAFF5D887D9.htm -->

# Use Unicode and Big Fonts (.NET)

AutoCAD supports the Unicode character-encoding standard. A Unicode font can contain 65,535 characters, with shapes for many languages. All of the AutoCAD SHX shape fonts that are shipped with the product support Unicode fonts. 

The text files for some alphabets contain thousands of non-ASCII characters. To accommodate such text, AutoCAD supports a special type of shape definition known as a Big Font file. You can set a style to use both regular and Big Font files. Specify normal fonts using the FileName property. Specify Big Fonts using the BigFontFileName property. 

Note: Font file names cannot contain commas. 

AutoCAD allows you to specify an alternate font to use when a specified font file cannot be located. Use the FONTALT system variable and the SetSystemVariable member method of the Application to change the alternate font used. 

## Change font files

The following example code changes the FileName and BigFontFileName properties. You need to replace the path information listed in this example with path and file names appropriate for your system. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ChangeFontFiles")]
    public static void ChangeFontFiles()
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
    
            // Change the font files used for both Big and Regular fonts
            acTextStyleTblRec.BigFontFileName = "C:/AutoCAD/Fonts/bigfont.shx";
            acTextStyleTblRec.FileName = "C:/AutoCAD/Fonts/italic.shx";
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ChangeFontFiles")> _
    Public Sub ChangeFontFiles()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the current text style for write
            Dim acTextStyleTblRec As TextStyleTableRecord
            acTextStyleTblRec = acTrans.GetObject(acCurDb.Textstyle, _
                                                  OpenMode.ForWrite)
    
            '' Change the font files used for both Big and Regular fonts
            acTextStyleTblRec.BigFontFileName = "C:\AutoCAD\Fonts\bigfont.shx"
            acTextStyleTblRec.FileName = "C:\AutoCAD\Fonts\italic.shx"
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ChangeFontFiles()
        ThisDrawing.ActiveTextStyle.BigFontFile = _
                      "C:/AutoCAD/Fonts/bigfont.shx"
     
        ThisDrawing.ActiveTextStyle.fontFile = _
                      "C:/AutoCAD/Fonts/italic.shx"
    End Sub
