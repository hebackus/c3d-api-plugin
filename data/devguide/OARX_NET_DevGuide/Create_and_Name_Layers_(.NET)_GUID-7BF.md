<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Create and Name Layers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7BF88244-D866-40D1-8C21-7DD1A2C633DF.htm -->

# Create and Name Layers (.NET)

You can create new layers and assign color and linetype properties to those layers. Each individual layer is part of the Layers table. Use the Add function to create a new layer and add it to the Layers table. 

You can assign a name to a layer when it is created. To change the name of a layer after it has been created, use the Name property. Layer names can include up to 255 characters and contain letters, digits, and the special characters dollar sign ($), hyphen (-), and underscore (_). 

## Create a new layer, assign it the color green, and add an object to the layer

The following code creates a new layer and circle object. The new layer is assigned the color green. The circle is assigned to the layer, and the color of the circle changes accordingly. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.Colors;
     
    [CommandMethod("CreateAndAssignALayer")]
    public static void CreateAndAssignALayer()
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
    
            string sLayerName = "Center";
    
            if (acLyrTbl.Has(sLayerName) == false)
            {
                using (LayerTableRecord acLyrTblRec = new LayerTableRecord())
                {
                    // Assign the layer the ACI color 3 and a name
                    acLyrTblRec.Color = Color.FromColorIndex(ColorMethod.ByAci, 3);
                    acLyrTblRec.Name = sLayerName;
    
                    // Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite);
    
                    // Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec);
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
                }
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
    Imports Autodesk.AutoCAD.Colors
     
    <CommandMethod("CreateAndAssignALayer")> _
    Public Sub CreateAndAssignALayer()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            Dim sLayerName As String = "Center"
    
            If acLyrTbl.Has(sLayerName) = False Then
                Using acLyrTblRec As LayerTableRecord = New LayerTableRecord()
    
                    '' Assign the layer the ACI color 3 and a name
                    acLyrTblRec.Color = Color.FromColorIndex(ColorMethod.ByAci, 3)
                    acLyrTblRec.Name = sLayerName
    
                    '' Upgrade the Layer table for write
                    acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                    '' Append the new layer to the Layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
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
    
    
    Sub CreateAssignALayer()
        ' Create a new layer and assign it the color red
        Dim layerObj As AcadLayer
        Set layerObj = ThisDrawing.Layers.Add("Center")
        layerObj.color = acRed
     
        ' Create a circle
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2: center(1) = 2: center(2) = 0
        radius = 1
        Set circleObj = ThisDrawing.ModelSpace. _
                        AddCircle(center, radius)
     
        ' Place the circle on the Center layer
        circleObj.Layer = "Center"
     
        circleObj.Update
    End Sub
