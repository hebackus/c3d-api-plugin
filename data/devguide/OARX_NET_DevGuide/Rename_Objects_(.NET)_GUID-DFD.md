<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Work With Named Objects (.NET) > Rename Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DFDAFCC3-6916-4B28-9AD8-BE537322B3DD.htm -->

# Rename Objects (.NET)

As your drawings become more complex, you can rename objects to keep the names meaningful or to avoid conflicts with names in other drawings you have inserted or attached. The Name property is used to get the current name or change the name of a named object. 

You can rename any named object except those reserved by AutoCAD, for example, layer 0 or the CONTINUOUS linetype. 

Names can be up to 255 characters long. In addition to letters and numbers, names can contain spaces (although AutoCAD removes spaces that appear directly before and after a name) and any special character not used by Microsoft® Windows® or AutoCAD for other purposes. Special characters that you cannot use include less-than and greater-than symbols (< >), forward slashes and backslashes (/ \\), quotation marks ("), colons (:), semicolons (;), question marks (?), commas (,), asterisks (*), vertical bars (|), equal signs (=), and single quotes ('). You also cannot use special characters created with Unicode fonts. 

## Rename a layer

This example creates a copy of layer "0" and renames the new layer to “MyLayer”. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("RenameLayer")]
    public static void RenameLayer()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Returns the layer table for the current database
            LayerTable acLyrTbl;
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                            OpenMode.ForWrite) as LayerTable;
    
            // Clone layer 0 (copy it and its properties) as a new layer
            LayerTableRecord acLyrTblRec;
            acLyrTblRec = acTrans.GetObject(acLyrTbl["0"],
                                            OpenMode.ForRead).Clone() as LayerTableRecord;
    
            // Change the name of the cloned layer
            acLyrTblRec.Name = "MyLayer";
    
            // Add the cloned layer to the Layer table and transaction
            acLyrTbl.Add(acLyrTblRec);
            acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
    
            // Save changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("RenameLayer")> _
    Public Sub RenameLayer()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Returns the layer table for the current database
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForWrite)
    
            '' Clone layer 0 (copy it and its properties) as a new layer
            Dim acLyrTblRec As LayerTableRecord
            acLyrTblRec = acTrans.GetObject(acLyrTbl("0"), _
                                            OpenMode.ForRead).Clone()
    
            '' Change the name of the cloned layer
            acLyrTblRec.Name = "MyLayer"
    
            '' Add the cloned layer to the Layer table and transaction
            acLyrTbl.Add(acLyrTblRec)
            acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
    
            '' Save changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub
