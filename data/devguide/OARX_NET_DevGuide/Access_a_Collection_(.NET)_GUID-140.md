<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Collection Objects (.NET) > Access a Collection (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-140CF8A1-FC7C-4E59-8290-D9C03B64CECC.htm -->

# Access a Collection (.NET)

Most collection and container objects are accessed through the Document or Database objects. The Document and Database objects contain a property to access an object or object id for most of the available Collection objects. For example, the following code defines a variable and retrieves the LayersTable object which represents the collection of Layers in the current drawing: 

## C#
    
    
    // Get the current document and start the Transaction Manager
    Database acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
    {
        // This example returns the layer table for the current database
        LayerTable acLyrTbl;
        acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                     OpenMode.ForRead) as LayerTable;
     
         // Dispose of the transaction
    }

## VB.NET
    
    
    '' Get the current document and start the Transaction Manager
    Dim acCurDb As Database = Application.DocumentManager.MdiActiveDocument.Database
    Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
        '' This example returns the layer table for the current database
        Dim acLyrTbl As LayerTable
        acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                     OpenMode.ForRead)
     
        '' Dispose of the transaction
    End Using

## VBA/ActiveX Code Reference
    
    
    Dim layerCollection as AcadLayers
    Set layerCollection = ThisDrawing.Layers
