<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Edit Dimensions (.NET) > Override Dimension Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B33DE16E-8D69-4B6C-A214-F254E69F241E.htm -->

# Override Dimension Text (.NET)

The dimension value that is displayed can be replaced using the DimensionText property. Using this property you can completely replace the displayed value of the dimension, or you can append text to the value. To represent the measured value in the override dimension text, use the character string “<>” in the text. 

## Modify dimension text

This example appends some text to the value so that both the string and the dimension value are displayed. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("OverrideDimensionText")]
    public static void OverrideDimensionText()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create the aligned dimension
            using (AlignedDimension acAliDim = new AlignedDimension())
            {
                acAliDim.XLine1Point = new Point3d(5, 3, 0);
                acAliDim.XLine2Point = new Point3d(10, 3, 0);
                acAliDim.DimLinePoint = new Point3d(7.5, 5, 0);
                acAliDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Override the dimension text
                acAliDim.DimensionText = "The value is <>";
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acAliDim);
                acTrans.AddNewlyCreatedDBObject(acAliDim, true);
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("OverrideDimensionText")> _
    Public Sub OverrideDimensionText()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create the aligned dimension
            Using acAliDim As AlignedDimension = New AlignedDimension()
                acAliDim.XLine1Point = New Point3d(5, 3, 0)
                acAliDim.XLine2Point = New Point3d(10, 3, 0)
                acAliDim.DimLinePoint = New Point3d(7.5, 5, 0)
                acAliDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Override the dimension text
                acAliDim.DimensionText = "The value is <>"
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acAliDim)
                acTrans.AddNewlyCreatedDBObject(acAliDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub OverrideDimensionText()
        Dim dimObj As AcadDimAligned
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
        Dim location(0 To 2) As Double
     
        ' Define the dimension
        point1(0) = 5#: point1(1) = 3#: point1(2) = 0#
        point2(0) = 10#: point2(1) = 3#: point2(2) = 0#
        location(0) = 7.5: location(1) = 5#: location(2) = 0#
     
        ' Create an aligned dimension object in model space
        Set dimObj = ThisDrawing.ModelSpace. _
                         AddDimAligned(point1, point2, location)
     
        ' Change the text string for the dimension
        dimObj.TextOverride = "The value is <>"
        dimObj.Update
    End Sub
