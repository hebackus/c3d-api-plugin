<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Ordinate Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7CA392C3-307C-4794-9EE6-30246672943F.htm -->

# Create Ordinate Dimensions (.NET)

Ordinate, or datum, dimensions measure the perpendicular distance from an origin point, called the datum, to a dimensioned feature, such as a hole in a part. These dimensions prevent escalating errors by maintaining accurate offsets of the features from the datum. 

Ordinate dimensions consist of an _X_ or _Y_ ordinate with a leader line. _X_ -datum ordinate dimensions measure the distance of a feature from the datum along the _X_ axis. _Y_ -datum ordinate dimensions measure the same distance along the _Y_ axis. AutoCAD uses the origin of the current user coordinate system (UCS) to determine the measured coordinates. The absolute value of the coordinate is used. 

The dimension text is aligned with the ordinate leader line regardless of the orientation defined by the current dimension style. You can accept the default text or override it with your own. 

You create an ordinate dimension by creating an instance of an OrdinateDimension object. When you create an instance of an OrdinateDimension object, its constructor can accept an optional set of parameters. The following parameters can be supplied when you create a new OrdinateDimension object: 

  * Use X axis (UsingXAxis property) 
  * Defining point (DefiningPoint property) 
  * Leader endpoint (LeaderEndPoint property) 
  * Dimension text (DimensionText property) 
  * Dimension style (DimensionStyleName or DimensionStyle properties) 

When passing values into the OrdinateDimension object constructor, the first value is a boolean flag which specifies whether the dimension is an _X_ -datum or _Y_ -datum ordinate dimension. If you enter TRUE, an _X_ -datum ordinate dimension is created. If you enter FALSE, a _Y_ -datum ordinate dimension is created. The UsingXAxis property can also be used to specify if an ordinate dimension is an _X_ -datum or _Y_ -datum. 

## Create an ordinate dimension

This example creates an ordinate dimension in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateOrdinateDimension")]
    public static void CreateOrdinateDimension()
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
    
            // Create an ordinate dimension
            using (OrdinateDimension acOrdDim = new OrdinateDimension())
            {
                acOrdDim.UsingXAxis = true;
                acOrdDim.DefiningPoint = new Point3d(5, 5, 0);
                acOrdDim.LeaderEndPoint = new Point3d(10, 5, 0);
                acOrdDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acOrdDim);
                acTrans.AddNewlyCreatedDBObject(acOrdDim, true);
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
     
    <CommandMethod("CreateOrdinateDimension")> _
    Public Sub CreateOrdinateDimension()
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
    
            '' Create an ordinate dimension
            Using acOrdDim As OrdinateDimension = New OrdinateDimension()
                acOrdDim.UsingXAxis = True
                acOrdDim.DefiningPoint = New Point3d(5, 5, 0)
                acOrdDim.LeaderEndPoint = New Point3d(10, 5, 0)
                acOrdDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acOrdDim)
                acTrans.AddNewlyCreatedDBObject(acOrdDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateOrdinateDimension()
        Dim dimObj As AcadDimOrdinate
        Dim definingPoint(0 To 2) As Double
        Dim leaderEndPoint(0 To 2) As Double
        Dim useXAxis As Boolean
     
        ' Define the dimension
        definingPoint(0) = 5
        definingPoint(1) = 5
        definingPoint(2) = 0
        leaderEndPoint(0) = 10
        leaderEndPoint(1) = 5
        leaderEndPoint(2) = 0
        useXAxis = True
     
        ' Create an ordinate dimension in model space
        Set dimObj = ThisDrawing.ModelSpace. _
                         AddDimOrdinate(definingPoint, _
                         leaderEndPoint, useXAxis)
     
        ZoomAll
    End Sub
