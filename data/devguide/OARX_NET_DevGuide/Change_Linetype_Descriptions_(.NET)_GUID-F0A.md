<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Change Linetype Descriptions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F0A370D6-0BEB-4EA1-A34B-53C93FEE9C84.htm -->

# Change Linetype Descriptions (.NET)

Linetypes can have a description associated with them. The description provides an ASCII representation of the linetype. You can assign or change a linetype description by using the AsciiDescription property. 

A linetype description can have up to 47 characters. The description can be a comment or a series of underscores, dots, dashes, and spaces to show a simple representation of the linetype pattern. 

## Change the description of a linetype

The following example changes the description of the current linetype. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ChangeLinetypeDescription")]
    public static void ChangeLinetypeDescription()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
     
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Linetype table record of the current linetype for write
            LinetypeTableRecord acLineTypTblRec;
            acLineTypTblRec = acTrans.GetObject(acCurDb.Celtype,
                                                OpenMode.ForWrite) as LinetypeTableRecord;
     
            // Change the description of the current linetype
            acLineTypTblRec.AsciiDescription = "Exterior Wall";
     
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ChangeLinetypeDescription")> _
    Public Sub ChangeLinetypeDescription()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
     
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
            '' Open the Linetype table record of the current linetype for write
            Dim acLineTypTblRec As LinetypeTableRecord
            acLineTypTblRec = acTrans.GetObject(acCurDb.Celtype, _
                                                OpenMode.ForWrite)
     
            '' Change the description of the current linetype
            acLineTypTblRec.AsciiDescription = "Exterior Wall"
     
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    ThisDrawing.ActiveLinetype.Description = "Exterior Wall"
