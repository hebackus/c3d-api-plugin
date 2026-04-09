<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Lock and Unlock Layers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-505CCDA2-7060-4180-929C-CD065AD840D2.htm -->

# Lock and Unlock Layers (.NET)

You cannot edit objects on a locked layer; however, they are still visible if the layer is on and thawed. You can make a locked layer current and you can add objects to it. You can freeze and turn off locked layers and change their associated colors and linetypes. 

Use the IsLocked property to lock or unlock a layer. If you input a value of TRUE, the layer is locked. If you input a value of FALSE, the layer is unlocked. 

## Lock a layer

This example creates a new layer called “ABC” and then locks the layer. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("LockLayer")]
    public static void LockLayer()
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
    
            string sLayerName = "ABC";
    
            if (acLyrTbl.Has(sLayerName) == false)
            {
                using (LayerTableRecord acLyrTblRec = new LayerTableRecord())
                {
                    // Assign the layer a name
                    acLyrTblRec.Name = sLayerName;
    
                    // Lock the layer
                    acLyrTblRec.IsLocked = true;
    
                    // Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite);
    
                    // Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec);
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
                }
            }
            else
            {
                LayerTableRecord acLyrTblRec = acTrans.GetObject(acLyrTbl[sLayerName],
                                                                 OpenMode.ForWrite) as LayerTableRecord;
    
                // Lock the layer
                acLyrTblRec.IsLocked = true;
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("LockLayer")> _
    Public Sub LockLayer()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            Dim sLayerName As String = "ABC"
    
            If acLyrTbl.Has(sLayerName) = False Then
                Using acLyrTblRec As LayerTableRecord = New LayerTableRecord()
    
                    '' Assign the layer a name
                    acLyrTblRec.Name = sLayerName
    
                    '' Lock the layer
                    acLyrTblRec.IsLocked = True
    
                    '' Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                    '' Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
            Else
                Dim acLyrTblRec As LayerTableRecord = acTrans.GetObject(acLyrTbl(sLayerName), _
                                                                        OpenMode.ForWrite)
    
                '' Lock the layer
                acLyrTblRec.IsLocked = True
            End If
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub LockLayer()
        ' Create a new layer called "ABC"
        Dim layerObj As AcadLayer
        Set layerObj = ThisDrawing.Layers.Add("ABC")
     
        ' Lock layer "ABC"
        layerObj.Lock = True
    End Sub
