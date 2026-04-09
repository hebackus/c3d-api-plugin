<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Radial Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C65CE759-DC39-47D3-8F39-7788059B011D.htm -->

# Create Radial Dimensions (.NET)

Radial dimensions measure the radii and diameters of arcs and circles. Radial and diametric dimensions are created by creating instances of RadialDimension and DiametricDimension objects. 

Different types of radial dimensions are created depending on the size of the circle or arc, the position of the dimension text, and the values in the DIMUPT, DIMTOFL, DIMFIT, DIMTIH, DIMTOH, DIMJUST, and DIMTAD dimension system variables. (System variables can be queried or set using the GetSystemVariable and SetSystemVariable methods.) 

For horizontal dimension text, if the angle of the dimension line is more than 15 degrees from horizontal, and is outside the circle or arc, AutoCAD draws a hook line, also called a landing or dogleg. The hook line is placed next to or below the dimension text, as shown in the following illustrations: 

When you create an instance of a RadialDimension object, you have the option to specify the center and chord points, the length of the leader, dimension text, and the dimension style to apply. Creating a DiametricDimension object is similar to a RadialDimension object except you specify chord and far chord points instead of a center and chord point. 

The LeaderLength property specifies the distance from the ChordPoint to the annotation text (or stop if no hook line is necessary). 

## Create a radial dimension

This example creates a radial dimension in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateRadialDimension")]
    public static void CreateRadialDimension()
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
    
            // Create the radial dimension
            using (RadialDimension acRadDim = new RadialDimension())
            {
                acRadDim.Center = new Point3d(0, 0, 0);
                acRadDim.ChordPoint = new Point3d(5, 5, 0);
                acRadDim.LeaderLength = 5;
                acRadDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRadDim);
                acTrans.AddNewlyCreatedDBObject(acRadDim, true);
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
     
    <CommandMethod("CreateRadialDimension")> _
    Public Sub CreateRadialDimension()
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
    
            '' Create the radial dimension
            Using acRadDim As RadialDimension = New RadialDimension()
                acRadDim.Center = New Point3d(0, 0, 0)
                acRadDim.ChordPoint = New Point3d(5, 5, 0)
                acRadDim.LeaderLength = 5
                acRadDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRadDim)
                acTrans.AddNewlyCreatedDBObject(acRadDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateRadialDimension()
        Dim dimObj As AcadDimRadial
        Dim center(0 To 2) As Double
        Dim chordPoint(0 To 2) As Double
        Dim leaderLen As Integer
     
        ' Define the dimension
        center(0) = 0
        center(1) = 0
        center(2) = 0
        chordPoint(0) = 5
        chordPoint(1) = 5
        chordPoint(2) = 0
        leaderLen = 5
     
        ' Create the radial dimension in model space
        Set dimObj = ThisDrawing.ModelSpace. _
                                      AddDimRadial(center, chordPoint, leaderLen)
        ZoomAll
    End Sub
