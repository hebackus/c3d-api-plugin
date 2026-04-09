<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Remove Layers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DF8A64D3-AE09-4BCE-B9E1-1B642DA4FCFF.htm -->

# Remove Layers (.NET)

You can remove a layer at any time during a drawing session. You cannot remove the current layer, layer 0, an xref-dependent layer, or a layer that contains objects. 

To remove a layer, use the Erase method. It is recommended to use the Purge function to verify that the layer can be purged, along with verifying that it is not layer 0, Defpoints, or the current layer. 

Note: Layers referenced by block definitions, along with the special layer named DEFPOINTS, cannot be deleted even if they do not contain visible objects. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("RemoveLayer")]
    public static void RemoveLayer()
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
    
            if (acLyrTbl.Has(sLayerName) == true)
            {
                // Check to see if it is safe to erase layer
                ObjectIdCollection acObjIdColl = new ObjectIdCollection();
                acObjIdColl.Add(acLyrTbl[sLayerName]);
                acCurDb.Purge(acObjIdColl);
    
                if (acObjIdColl.Count > 0)
                {
                    LayerTableRecord acLyrTblRec;
                    acLyrTblRec = acTrans.GetObject(acObjIdColl[0],
                                                    OpenMode.ForWrite) as LayerTableRecord;
    
                    try
                    {
                        // Erase the unreferenced layer
                        acLyrTblRec.Erase(true);
    
                        // Save the changes and dispose of the transaction
                        acTrans.Commit();
                    }
                    catch (Autodesk.AutoCAD.Runtime.Exception Ex)
                    {
                        // Layer could not be deleted
                        Application.ShowAlertDialog("Error:\n" + Ex.Message);
                    }
                }
            }
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("RemoveLayer")> _
    Public Sub RemoveLayer()
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
    
            If acLyrTbl.Has(sLayerName) = True Then
                '' Check to see if it is safe to erase layer
                Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
                acObjIdColl.Add(acLyrTbl(sLayerName))
                acCurDb.Purge(acObjIdColl)
    
                If acObjIdColl.Count > 0 Then
                    Dim acLyrTblRec As LayerTableRecord
                    acLyrTblRec = acTrans.GetObject(acObjIdColl(0), OpenMode.ForWrite)
    
                    Try
                        '' Erase the unreferenced layer
                        acLyrTblRec.Erase(True)
    
                        '' Save the changes and dispose of the transaction
                        acTrans.Commit()
                    Catch Ex As Autodesk.AutoCAD.Runtime.Exception
                        '' Layer could not be deleted
                        Application.ShowAlertDialog("Error:\n" + Ex.Message)
                    End Try
                End If
            End If
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub RemoveLayer()
        On Error Resume Next
     
        Dim layerObj As AcadLayer
        Set layerObj = ThisDrawing.Layers("ABC")
     
        layerObj.Delete
    End Sub
