<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Assign Color to a Layer (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4C6504CF-3AEE-4CBF-97DE-55BDF2515192.htm -->

# Assign Color to a Layer (.NET)

Each layer can have its own color assigned to it. Colors for a layer are identified by the Color object which is part of the Colors namespace. This object can hold an RGB value, ACI number (an integer from 1 to 255), or a color book color. 

To assign a color to a layer, use the Color property. 

Note: Objects such as lines and circles support two different properties to control their current color. The Color property is used to assign an RGB value, ACI number, or a color book color, while the ColorIndex property only supports ACI numbers. 

If you use the ACI color 0 or ByBlock, AutoCAD draws new objects in the default color (white or black, depending on your configuration) until they are grouped into a block. When the block is inserted, the objects in the block inherit the current property setting. 

If you use the ACI color 256 or ByLayer, new objects inherit the color of the layer upon which they are drawn. 

## Set the color of a layer

The following example creates three new layers and each is assigned a different color using each of the three color methods. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Colors;
     
    [CommandMethod("SetLayerColor")]
    public static void SetLayerColor()
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
    
            // Define an array of layer names
            string[] sLayerNames = new string[3];
            sLayerNames[0] = "ACIRed";
            sLayerNames[1] = "TrueBlue";
            sLayerNames[2] = "ColorBookYellow";
    
            // Define an array of colors for the layers
            Color[] acColors = new Color[3];
            acColors[0] = Color.FromColorIndex(ColorMethod.ByAci, 1);
            acColors[1] = Color.FromRgb(23, 54, 232);
            acColors[2] = Color.FromNames("PANTONE Yellow 0131 C",
                                          "PANTONE+ Pastels & Neons Coated");
    
            int nCnt = 0;
    
            // Add or change each layer in the drawing
            foreach (string sLayerName in sLayerNames)
            {
                if (acLyrTbl.Has(sLayerName) == false)
                {
                    using (LayerTableRecord acLyrTblRec = new LayerTableRecord())
                    {
                        // Assign the layer a name
                        acLyrTblRec.Name = sLayerName;
    
                        // Set the color of the layer
                        acLyrTblRec.Color = acColors[nCnt];
    
                        // Upgrade the Layer table for write
                        if (acLyrTbl.IsWriteEnabled == false) acTrans.GetObject(acCurDb.LayerTableId, 
                                                                                OpenMode.ForWrite);
    
                        // Append the new layer to the Layer table and the transaction
                        acLyrTbl.Add(acLyrTblRec);
                        acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
                    }
                }
                else
                {
                    // Open the layer if it already exists for write
                    LayerTableRecord acLyrTblRec = acTrans.GetObject(acLyrTbl[sLayerName],
                                                                     OpenMode.ForWrite) as LayerTableRecord;
    
                    // Set the color of the layer
                    acLyrTblRec.Color = acColors[nCnt];
                }
    
                nCnt = nCnt + 1;
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Colors
     
    <CommandMethod("SetLayerColor")> _
    Public Sub SetLayerColor()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            '' Define an array of layer names
            Dim sLayerNames(2) As String
            sLayerNames(0) = "ACIRed"
            sLayerNames(1) = "TrueBlue"
            sLayerNames(2) = "ColorBookYellow"
    
            '' Define an array of colors for the layers
            Dim acColors(2) As Color
            acColors(0) = Color.FromColorIndex(ColorMethod.ByAci, 1)
            acColors(1) = Color.FromRgb(23, 54, 232)
            acColors(2) = Color.FromNames("PANTONE Yellow 0131 C", _
                                          "PANTONE+ Pastels & Neons Coated")
    
            Dim nCnt As Integer = 0
    
            '' Add or change each layer in the drawing
            For Each sLayerName As String In sLayerNames
    
                If acLyrTbl.Has(sLayerName) = False Then
                    Using acLyrTblRec As LayerTableRecord = New LayerTableRecord()
    
                        '' Assign the layer a name
                        acLyrTblRec.Name = sLayerName
    
                        '' Set the color of the layer
                        acLyrTblRec.Color = acColors(nCnt)
    
                        '' Upgrade the Layer table for write
                        If acLyrTbl.IsWriteEnabled = False Then acTrans.GetObject(acCurDb.LayerTableId, 
                                                                                  OpenMode.ForWrite)
    
                        '' Append the new layer to the Layer table and the transaction
                        acLyrTbl.Add(acLyrTblRec)
                        acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                    End Using
                Else
                    '' Open the layer if it already exists for write
                    Dim acLyrTblRec As LayerTableRecord = acTrans.GetObject(acLyrTbl(sLayerName), _
                                                                            OpenMode.ForWrite)
    
                    '' Set the color of the layer
                    acLyrTblRec.Color = acColors(nCnt)
                End If
    
                nCnt = nCnt + 1
            Next
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SetLayerColor()
        Dim layerObj As AcadLayer
     
        ' Define an array of layer names
        Dim sLayerNames(2) As String
        sLayerNames(0) = "ACIRed"
        sLayerNames(1) = "TrueBlue"
        sLayerNames(2) = "ColorBookYelow"
     
        ' Define an array of colors
        Dim colorObj(2) As New AcadAcCmColor
     
        colorObj(0).ColorMethod = acColorMethodByACI
        colorObj(0).ColorIndex = acRed
        Call colorObj(1).SetRGB(23, 54, 232)
        Call colorObj(2).SetColorBookColor("PANTONE+ Pastels & Neons Coated", _
                                           "PANTONE Yellow 0131 C")
     
        Dim nCnt As Integer
     
        ' Step through each layer name and create a new layer
        For Each sLayerName In sLayerNames
           Set layerObj = ThisDrawing.Layers.Add(sLayerName)
           layerObj.TrueColor = colorObj(nCnt)
     
           nCnt = nCnt + 1
        Next
    End Sub
