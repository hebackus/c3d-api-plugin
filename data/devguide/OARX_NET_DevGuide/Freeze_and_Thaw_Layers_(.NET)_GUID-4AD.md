<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Freeze and Thaw Layers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4ADF80DD-5BEF-4C28-90A9-76FDA8E2E804.htm -->

# Freeze and Thaw Layers (.NET)

You can freeze layers to speed up display changes, improve object selection performance, and reduce regeneration time for complex drawings. AutoCAD does not display, plot, or regenerate objects on frozen layers. Freeze the layers that you will not be working with for long periods of time. When you “thaw” a frozen layer, AutoCAD regenerates and displays the objects on that layer. 

Use the IsFrozen property to freeze or thaw a layer. If you input a value of TRUE, the layer is frozen. If you input a value of FALSE, the layer is thawed. 

## Freeze a layer

This example creates a new layer called “ABC” and then freezes the layer. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("FreezeLayer")]
    public static void FreezeLayer()
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
    
                    // Freeze the layer
                    acLyrTblRec.IsFrozen = true;
    
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
    
                // Freeze the layer
                acLyrTblRec.IsFrozen = true;
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("FreezeLayer")> _
    Public Sub FreezeLayer()
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
    
                    '' Freeze the layer
                    acLyrTblRec.IsFrozen = True
    
                    '' Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                    '' Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
            Else
                Dim acLyrTblRec As LayerTableRecord = acTrans.GetObject(acLyrTbl(sLayerName), _
                                                                        OpenMode.ForWrite)
    
                '' Freeze the layer
                acLyrTblRec.IsFrozen = True
            End If
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FreezeLayer()
        ' Create a new layer called "ABC"
        Dim layerObj As AcadLayer
        Set layerObj = ThisDrawing.Layers.Add("ABC")
     
        ' Freeze layer "ABC"
        layerObj.Freeze = True
    End Sub
