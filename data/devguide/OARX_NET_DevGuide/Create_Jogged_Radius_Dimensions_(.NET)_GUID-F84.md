<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Jogged Radius Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F84FB751-B4A3-4A19-9EB2-B2977AA000A2.htm -->

# Create Jogged Radius Dimensions (.NET)

Jogged radius dimensions measure the radius of an object and displays the dimension text with a radius symbol in front of it. You might use a jogged dimension over a radial dimension object when: 

  * An object’s center point is located outside of the layout or is over an area of the model that does not have enough room for a radial dimension 
  * An object has a large radius 

You create a jogged radius dimension by creating an instance of a RadialDimensionLarge object. When you create an instance of a RadialDimensionLarge object, its constructors can optionally accept a set parameters. The following parameters can be supplied when you create a new RadialDimensionLarge object: 

  * Center point (Center property) 
  * Chord point (ChordPoint property) 
  * Override center point (OverrideCenter property) 
  * Position of the jog lines (JogPoint property) 
  * Angle of the jog lines (JogAngle property) 
  * Dimension text (DimensionText property) 
  * Dimension style (DimensionStyleName or DimensionStyle properties) 

## Create a jogged radius dimension

This example creates a jogged radius dimension in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateJoggedDimension")]
    public static void CreateJoggedDimension()
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
    
            // Create a large radius dimension
            using (RadialDimensionLarge acRadDimLrg = new RadialDimensionLarge())
            {
                acRadDimLrg.Center = new Point3d(-3, -4, 0);
                acRadDimLrg.ChordPoint = new Point3d(2, 7, 0);
                acRadDimLrg.OverrideCenter = new Point3d(0, 2, 0);
                acRadDimLrg.JogPoint = new Point3d(1, 4.5, 0);
                acRadDimLrg.JogAngle = 0.707;
                acRadDimLrg.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRadDimLrg);
                acTrans.AddNewlyCreatedDBObject(acRadDimLrg, true);
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
     
    <CommandMethod("CreateJoggedDimension")> _
    Public Sub CreateJoggedDimension()
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
    
            '' Create a large radius dimension
            Using acRadDimLrg As RadialDimensionLarge = New RadialDimensionLarge()
                acRadDimLrg.Center = New Point3d(-3, -4, 0)
                acRadDimLrg.ChordPoint = New Point3d(2, 7, 0)
                acRadDimLrg.OverrideCenter = New Point3d(0, 2, 0)
                acRadDimLrg.JogPoint = New Point3d(1, 4.5, 0)
                acRadDimLrg.JogAngle = 0.707
                acRadDimLrg.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRadDimLrg)
                acTrans.AddNewlyCreatedDBObject(acRadDimLrg, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateJoggedDimension()
        Dim dimObj As AcadDimRadialLarge
        Dim centerPoint(0 To 2) As Double
        Dim chordPoint(0 To 2) As Double
        Dim centerOverPoint(0 To 2) As Double
        Dim jogPoint(0 To 2) As Double
        Dim jogAngle As Double
     
        ' Define the dimension
        centerPoint(0) = -3: centerPoint(1) = -4: centerPoint(2) = 0
        chordPoint(0) = 2: chordPoint(1) = 7: chordPoint(2) = 0
        centerOverPoint(0) = 0: centerOverPoint(1) = 2: centerOverPoint(2) = 0
        jogPoint(0) = 1: jogPoint(1) = 4.5: jogPoint(2) = 0
        jogAngle = 0.707
     
        ' Create the jogged dimension in Model space
        Set dimObj = ThisDrawing.ModelSpace. _
                         AddDimRadialLarge(centerPoint, chordPoint, _
                                           centerOverPoint, jogPoint, _
                                           jogAngle)
     
        ZoomAll
    End Sub
