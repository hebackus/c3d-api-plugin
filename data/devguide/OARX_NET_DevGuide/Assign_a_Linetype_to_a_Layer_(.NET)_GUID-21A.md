<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Assign a Linetype to a Layer (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-21AFAAC8-5B07-4DEB-B45E-980AECC05168.htm -->

# Assign a Linetype to a Layer (.NET)

When you are defining layers, linetypes provide another way to convey visual information. A linetype is a repeating pattern of dashes, dots, and blank spaces you can use to distinguish the purpose of one line from another. 

The linetype name and definition describe the particular dash-dot sequence, the relative lengths of dashes and blank spaces, and the characteristics of any included text or shapes. 

Use the Linetype property to assign a linetype to a layer. This property takes the name of the linetype as input. 

Note: Before a linetype can be assigned to a layer it must be defined in the drawing first. 

## Set the linetype for a layer

The following example creates a new layer named "ABC" and assigns it the "Center" linetype. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("SetLayerLinetype")]
    public static void SetLayerLinetype()
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
    
                    // Open the Layer table for read
                    LinetypeTable acLinTbl;
                    acLinTbl = acTrans.GetObject(acCurDb.LinetypeTableId,
                                                 OpenMode.ForRead) as LinetypeTable;
    
                    if (acLinTbl.Has("Center") == true)
                    {
                        // Set the linetype for the layer
                        acLyrTblRec.LinetypeObjectId = acLinTbl["Center"];
                    }
    
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
                                                                 OpenMode.ForRead) as LayerTableRecord;
    
                // Open the Layer table for read
                LinetypeTable acLinTbl;
                acLinTbl = acTrans.GetObject(acCurDb.LinetypeTableId,
                                             OpenMode.ForRead) as LinetypeTable;
    
                if (acLinTbl.Has("Center") == true)
                {
                    // Upgrade the Layer Table Record for write
                    acTrans.GetObject(acLyrTbl[sLayerName], OpenMode.ForWrite);
    
                    // Set the linetype for the layer
                    acLyrTblRec.LinetypeObjectId = acLinTbl["Center"];
                }
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("SetLayerLinetype")> _
    Public Sub SetLayerLinetype()
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
    
                    '' Open the Layer table for read
                    Dim acLinTbl As LinetypeTable
                    acLinTbl = acTrans.GetObject(acCurDb.LinetypeTableId, _
                                                 OpenMode.ForRead)
    
                    If acLinTbl.Has("Center") = True Then
                        '' Set the linetype for the layer
                        acLyrTblRec.LinetypeObjectId = acLinTbl("Center")
                    End If
    
                    '' Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                    '' Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
            Else
                Dim acLyrTblRec As LayerTableRecord = acTrans.GetObject(acLyrTbl(sLayerName), _
                                                                        OpenMode.ForRead)
    
                '' Open the Layer table for read
                Dim acLinTbl As LinetypeTable
                acLinTbl = acTrans.GetObject(acCurDb.LinetypeTableId, _
                                             OpenMode.ForRead)
    
                If acLinTbl.Has("Center") = True Then
                    '' Upgrade the Layer Table Record for write
                    acTrans.GetObject(acLyrTbl(sLayerName), OpenMode.ForWrite)
    
                    '' Set the linetype for the layer
                    acLyrTblRec.LinetypeObjectId = acLinTbl("Center")
                End If
            End If
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SetLayerLinetype()
        On Error Resume Next
        Dim layerObj As AcadLayer
     
        Set layerObj = ThisDrawing.Layers.Add("ABC")
        layerObj.Linetype = "Center"
    End Sub
