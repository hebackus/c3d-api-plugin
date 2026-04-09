<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Turn Layers On and Off (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-09BBF8AE-B581-499D-AFF0-41F53C1B6ACC.htm -->

# Turn Layers On and Off (.NET)

Layers in which are turned off are regenerated with the drawing but are not displayed or plotted. By turning layers off, you avoid regenerating the drawing every time you thaw a layer. When you turn a layer on that has been turned off, AutoCAD redraws the objects on that layer. 

Use the IsOff property on the LayerTableRecord object that represents the layer you want to turn on or off. If you input a value of TRUE, the layer is turned off. If you input a value of FALSE, the layer is turned on. 

## Turn off a layer

This example creates a new layer and turns it off, and then adds a circle to the layer so that the circle is no longer visible. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("TurnLayerOff")]
    public static void TurnLayerOff()
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
    
                    // Turn the layer off
                    acLyrTblRec.IsOff = true;
    
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
    
                // Turn the layer off
                acLyrTblRec.IsOff = true;
            }
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle object
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 1;
                acCirc.Layer = sLayerName;
    
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("TurnLayerOff")> _
    Public Sub TurnLayerOff()
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
    
                    '' Turn the layer off
                    acLyrTblRec.IsOff = True
    
                    '' Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                    '' Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
            Else
                Dim acLyrTblRec As LayerTableRecord = acTrans.GetObject(acLyrTbl(sLayerName), _
                                                                        OpenMode.ForWrite)
    
                '' Turn the layer off
                acLyrTblRec.IsOff = True
            End If
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle object
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 1
                acCirc.Layer = sLayerName
    
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub TurnLayerOff()
        ' Create a new layer called "ABC"
        Dim layerObj As AcadLayer
        Set layerObj = ThisDrawing.Layers.Add("ABC")
     
        ' Turn off layer "ABC"
        layerObj.LayerOn = False
     
        ' Create a circle
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2: center(1) = 2: center(2) = 0
        radius = 1
        Set circleObj = ThisDrawing.ModelSpace. _
                                      AddCircle(center, radius)
     
        ' Assign the circle to the "ABC" layer
        circleObj.Layer = "ABC"
        circleObj.Update
     
        ThisDrawing.Regen acActiveViewport
    End Sub
