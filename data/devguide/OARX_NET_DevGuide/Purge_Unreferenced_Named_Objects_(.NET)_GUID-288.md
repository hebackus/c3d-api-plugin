<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Work With Named Objects (.NET) > Purge Unreferenced Named Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-288B4394-C51F-48CC-8B8C-A27873CFFDC1.htm -->

# Purge Unreferenced Named Objects (.NET)

Unreferenced named objects can be purged from a database at any time. You cannot purge named objects that are referenced by other objects. For example, a font file might be referenced by a text style or a layer might be referenced by the objects on that layer. Purging reduces the size of a drawing file when saved to disk. 

Unreferenced objects are purged from a drawing database with the Purge method. The Purge method requires a list of objects you want to purge in the form of an ObjectIdCollection or ObjectIdGraph objects. The ObjectIdCollection or ObjectIdGraph objects passed into the Purge method are updated with the objects in which can be erased from the database. After the call to Purge, you must erase each individual object returned. 

## Purge all unreferenced layers

The following example demonstrates how to purge all unreferenced layers from a database. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("PurgeUnreferencedLayers")]
    public static void PurgeUnreferencedLayers()
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
    
            // Create an ObjectIdCollection to hold the object ids for each table record
            ObjectIdCollection acObjIdColl = new ObjectIdCollection();
    
            // Step through each layer and add iterator to the ObjectIdCollection
            foreach (ObjectId acObjId in acLyrTbl)
            {
                acObjIdColl.Add(acObjId);
            }
    
            // Remove the layers that are in use and return the ones that can be erased
            acCurDb.Purge(acObjIdColl);
    
            // Step through the returned ObjectIdCollection
            // and erase each unreferenced layer
            foreach (ObjectId acObjId in acObjIdColl)
            {
                SymbolTableRecord acSymTblRec;
                acSymTblRec = acTrans.GetObject(acObjId,
                                                OpenMode.ForWrite) as SymbolTableRecord;
    
                try
                {
                    // Erase the unreferenced layer
                    acSymTblRec.Erase(true);
                }
                catch (Autodesk.AutoCAD.Runtime.Exception Ex)
                {
                    // Layer could not be deleted
                    Application.ShowAlertDialog("Error:\n" + Ex.Message);
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
     
    <CommandMethod("PurgeUnreferencedLayers")> _
    Public Sub PurgeUnreferencedLayers()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            '' Create an ObjectIdCollection to hold the object ids for each table record
            Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
    
            '' Step through each layer and add it to the ObjectIdCollection
            For Each acObjId As ObjectId In acLyrTbl
                acObjIdColl.Add(acObjId)
            Next
    
            '' Remove the layers that are in use and return the ones that can be erased
            acCurDb.Purge(acObjIdColl)
    
            '' Step through the returned ObjectIdCollection
            For Each acObjId As ObjectId In acObjIdColl
                Dim acSymTblRec As SymbolTableRecord
                acSymTblRec = acTrans.GetObject(acObjId, _
                                                OpenMode.ForWrite)
    
                Try
                    '' Erase the unreferenced layer
                    acSymTblRec.Erase(True)
                Catch Ex As Autodesk.AutoCAD.Runtime.Exception
                    '' Layer could not be deleted
                    Application.ShowAlertDialog("Error:" & vbLf & Ex.Message)
                End Try
            Next
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Cross Reference

In the ActiveX Automation library you would use the PurgeAll method to remove all unreferenced named objects and it would identify which objects can be removed. However, with the AutoCAD .NET API you need to supply which objects you would like to purge and then the Purge method returns to you which ones actually can be. So there is a bit more work involved when working with the AutoCAD .NET API to purge all unreferenced named objects from a database. 
    
    
    ThisDrawing.PurgeAll
