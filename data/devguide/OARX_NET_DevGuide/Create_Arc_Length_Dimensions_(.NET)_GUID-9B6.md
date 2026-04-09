<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Arc Length Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9B6305F6-7889-4C7A-A8F1-0F44A8510A15.htm -->

# Create Arc Length Dimensions (.NET)

Arc length dimensions measure the length along an arc and displays the dimension text with an arc symbol that is either above or proceeds it. You might use an arc length dimension when you need to dimension the actual length of an arc instead of just distance between its start and end points. 

You create an arc length radius dimension by creating an instance of an ArcDimension object. When you create an instance of an ArcDimension object, it requires a set of parameters that define the dimension. The following parameters must be supplied when you create a new ArcDimension object: 

  * Center point (Center property) 
  * Extension line 1 point (XLine1Point property) 
  * Extension line 2 point (XLine2Point property) 
  * Arc point (ArcPoint property) 
  * Dimension text (DimensionText property) 
  * Dimension style (DimensionStyleName or DimensionStyle properties) 

Note: The DIMARCSYM system variable controls if an arc symbol is displayed and where it is displayed in relation to the dimension text. 

## Create an arc length dimension

This example creates an arc length dimension in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateArcLengthDimension")]
    public static void CreateArcLengthDimension()
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
    
            // Create an arc length dimension
            using (ArcDimension acArcDim = new ArcDimension(new Point3d(4.5, 1.5, 0),
                                                            new Point3d(8, 4.25, 0),
                                                            new Point3d(0, 2, 0),
                                                            new Point3d(5, 7, 0),
                                                            "<>",
                                                            acCurDb.Dimstyle))
            {
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acArcDim);
                acTrans.AddNewlyCreatedDBObject(acArcDim, true);
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
     
    <CommandMethod("CreateArcLengthDimension")> _
    Public Sub CreateArcLengthDimension()
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
    
            '' Create an arc length dimension
            Using acArcDim As ArcDimension = New ArcDimension(New Point3d(4.5, 1.5, 0), _
                                                              New Point3d(8, 4.25, 0), _
                                                              New Point3d(0, 2, 0), _
                                                              New Point3d(5, 7, 0), _
                                                              "<>", _
                                                              acCurDb.Dimstyle)
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acArcDim)
                acTrans.AddNewlyCreatedDBObject(acArcDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateArcLengthDimension()
        Dim dimObj As AcadDimArcLength
        Dim arcCenterPoint(0 To 2) As Double
        Dim firstPoint(0 To 2) As Double
        Dim secondPoint(0 To 2) As Double
        Dim arcPoint(0 To 2) As Double
     
        ' Define the dimension
        arcCenterPoint(0) = 4.5: arcCenterPoint(1) = 1.5: arcCenterPoint(2) = 0
        firstPoint(0) = 8: firstPoint(1) = 4.25: firstPoint(2) = 0
        secondPoint(0) = 0: secondPoint(1) = 2: secondPoint(2) = 0
        arcPoint(0) = 5: arcPoint(1) = 7: arcPoint(2) = 0
     
        ' Create the arc length dimension in Model space
        Set dimObj = ThisDrawing.ModelSpace. _
                         AddDimArc(arcCenterPoint, firstPoint, _
                         secondPoint, arcPoint)
     
        ZoomAll
    End Sub
