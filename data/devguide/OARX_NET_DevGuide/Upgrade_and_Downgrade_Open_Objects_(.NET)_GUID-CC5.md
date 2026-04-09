<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Upgrade and Downgrade Open Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CC5CC229-B122-4897-A8DA-5C5ADADB0F38.htm -->

# Upgrade and Downgrade Open Objects (.NET)

An object's current open mode can be changed from read to write or write to read by upgrading or downgrading the object. 

These methods can be used to upgrade or downgrade a previously opened object: 

  * Transaction.GetObject method – If the object was opened with the Transaction.GetObject method, use the method to reopen the object with the desired new open mode. 
  * UpgradeOpen and DowngradeOpen methods – If the object was opened with the Open method, or the OpenCloseTransaction.GetObject, use the UpgradeOpen method to change the object’s open mode from read to write or DowngradeOpen method to change the object’s open mode from write to read. You do not need to pair a call to DowngradeOpen with each UpgradeOpen, since closing of an object or disposing of a transaction will sufficiently cleanup the open state of an object. 

It is recommended to open an object with the mode that best matches how the object will be used, as it is more efficient to open an object for read and query the object’s properties than it is to open the object for write and query the object’s properties. If you are uncertain whether an object might need to be modified, it is best to open the object for read and then upgrade it for write as this helps to reduce the overhead of your program. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("FreezeDoorLayer")]
    public static void FreezeDoorLayer()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Layer table for read
            LayerTable acLyrTbl;
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                         OpenMode.ForRead) as LayerTable;
    
            // Step through each layer and update those that start with 'Door'
            foreach (ObjectId acObjId in acLyrTbl)
            {
                // Open the Layer table record for read
                LayerTableRecord acLyrTblRec;
                acLyrTblRec = acTrans.GetObject(acObjId,
                                                OpenMode.ForRead) as LayerTableRecord;
    
                // Check to see if the layer's name starts with 'Door' 
                if (acLyrTblRec.Name.StartsWith("Door",
                                                StringComparison.OrdinalIgnoreCase) == true)
                {
                    // Check to see if the layer is current, if so then do not freeze it
                    if (acLyrTblRec.ObjectId != acCurDb.Clayer)
                    {
                        // Change from read to write mode
                        acTrans.GetObject(acObjId, OpenMode.ForWrite);
    
                        // Freeze the layer
                        acLyrTblRec.IsFrozen = true;
                    }
                }
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("FreezeDoorLayer")> _
    Public Sub FreezeDoorLayer()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForRead)
    
            '' Step through each layer and update those that start with 'Door'
            For Each acObjId As ObjectId In acLyrTbl
                '' Open the Layer table record for read
                Dim acLyrTblRec As LayerTableRecord
                acLyrTblRec = acTrans.GetObject(acObjId, OpenMode.ForRead)
    
                '' Check to see if the layer's name starts with 'Door' 
                If (acLyrTblRec.Name.StartsWith("Door", _
                                                StringComparison.OrdinalIgnoreCase) = True) Then
                    '' Check to see if the layer is current, if so then do not freeze it
                    If acLyrTblRec.ObjectId <> acCurDb.Clayer Then
                        '' Change from read to write mode
                        acTrans.GetObject(acObjId, OpenMode.ForWrite)
    
                        '' Freeze the layer
                        acLyrTblRec.IsFrozen = True
                    End If
                End If
            Next
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub
