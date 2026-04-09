<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Angular Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3E7552CA-56FA-427C-9419-3F1999702F5C.htm -->

# Create Angular Dimensions (.NET)

Angular dimensions measure the angle between two lines or three points. For example, you can use them to measure the angle between two radii of a circle. The dimension line forms an arc. Angular dimensions are created by creating instances of LineAngularDimension2 or Point3AngularDimension objects. 

  * **LineAngularDimension2.** Represents an angular dimension defined by two lines. 
  * **Point3AngularDimension.** Represents an angular dimension defined by three points. 

When you create an instance of a LineAngularDimension2 or Point3AngularDimension object, the constructors can optionally accept a set parameters. The following parameters can be supplied when you create a new LineAngularDimension2 object: 

  * Extension line 1 start point (XLine1Start property) 
  * Extension line 1 end point (XLine1End property) 
  * Extension line 2 start point (XLine2Start property) 
  * Extension line 1 end point (XLine2End property) 
  * Arc point (ArcPoint property) 
  * Dimension text (DimensionText property) 
  * Dimension style (DimensionStyleName or DimensionStyle properties) 

The following parameters can be supplied when you create a new Point3AngularDimension object: 

  * Center point (CenterPoint property) 
  * Extension line 1point (XLine1Point property) 
  * Extension line 2 point (XLine2Point property) 
  * Arc point (ArcPoint property) 
  * Dimension text (DimensionText property) 
  * Dimension style (DimensionStyleName or DimensionStyle properties) 

## Create an angular dimension

This example creates an angular dimension in model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateAngularDimension")]
    public static void CreateAngularDimension()
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
    
            // Create an angular dimension
            using (LineAngularDimension2 acLinAngDim = new LineAngularDimension2())
            {
                acLinAngDim.XLine1Start = new Point3d(0, 5, 0);
                acLinAngDim.XLine1End = new Point3d(1, 7, 0);
                acLinAngDim.XLine2Start = new Point3d(0, 5, 0);
                acLinAngDim.XLine2End = new Point3d(1, 3, 0);
                acLinAngDim.ArcPoint = new Point3d(3, 5, 0);
                acLinAngDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acLinAngDim);
                acTrans.AddNewlyCreatedDBObject(acLinAngDim, true);
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
     
    <CommandMethod("CreateAngularDimension")> _
    Public Sub CreateAngularDimension()
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
    
            '' Create an angular dimension
            Using acLinAngDim As LineAngularDimension2 = New LineAngularDimension2()
                acLinAngDim.XLine1Start = New Point3d(0, 5, 0)
                acLinAngDim.XLine1End = New Point3d(1, 7, 0)
                acLinAngDim.XLine2Start = New Point3d(0, 5, 0)
                acLinAngDim.XLine2End = New Point3d(1, 3, 0)
                acLinAngDim.ArcPoint = New Point3d(3, 5, 0)
                acLinAngDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acLinAngDim)
                acTrans.AddNewlyCreatedDBObject(acLinAngDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateAngularDimension()
        Dim dimObj As AcadDimAngular
        Dim angVert(0 To 2) As Double
        Dim FirstPoint(0 To 2) As Double
        Dim SecondPoint(0 To 2) As Double
        Dim TextPoint(0 To 2) As Double
     
        ' Define the dimension
        angVert(0) = 0
        angVert(1) = 5
        angVert(2) = 0
        FirstPoint(0) = 1
        FirstPoint(1) = 7
        FirstPoint(2) = 0
        SecondPoint(0) = 1
        SecondPoint(1) = 3
        SecondPoint(2) = 0
        TextPoint(0) = 3
        TextPoint(1) = 5
        TextPoint(2) = 0
     
        ' Create the angular dimension in model space
        Set dimObj = ThisDrawing.ModelSpace. _
                        AddDimAngular(angVert, FirstPoint, SecondPoint, TextPoint)
        ZoomAll
    End Sub
