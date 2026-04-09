<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Work With Regions (.NET) > Create Composite Regions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-684E602E-3555-4370-BCDC-1CE594676C43.htm -->

# Create Composite Regions (.NET)

You can create composite regions by subtracting, combining, or finding the intersection of regions or 3D solids. You can then extrude or revolve composite regions to create complex solids. To create a composite region, use the BooleanOperation method. 

## Subtract regions

When you subtract one region from another, you call the BooleanOperation method from the first region. This is the region from which you want to subtract. For example, to calculate how much carpeting is needed for a floor plan, call the BooleanOperation method from the outer boundary of the floor space and use the non-carpeted areas, such as pillars and counters, as the object in the Boolean parameter list. 

## Unite regions

To unite regions, call the BooleanOperation method and use the constant BooleanOperationType.BoolUnite for the operation instead of BooleanOperationType.BoolSubtract. You can combine regions in any order to unite them. 

## Find the intersection of two regions

To find the intersection of two regions, use the constant BooleanOperationType.BoolIntersect. You can combine regions in any order to intersect them. 

## Create a composite region

The following example creates two regions from two circles and then subtracts the smaller region from the large one to create a wheel. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateCompositeRegions")]
    public static void CreateCompositeRegions()
    {
        // Get the current document and database
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
    
            // Create two in memory circles
            using (Circle acCirc1 = new Circle())
            {
                acCirc1.Center = new Point3d(4, 4, 0);
                acCirc1.Radius = 2;
    
                using (Circle acCirc2 = new Circle())
                {
                    acCirc2.Center = new Point3d(4, 4, 0);
                    acCirc2.Radius = 1;
    
                    // Adds the circle to an object array
                    DBObjectCollection acDBObjColl = new DBObjectCollection();
                    acDBObjColl.Add(acCirc1);
                    acDBObjColl.Add(acCirc2);
    
                    // Calculate the regions based on each closed loop
                    DBObjectCollection myRegionColl = new DBObjectCollection();
                    myRegionColl = Region.CreateFromCurves(acDBObjColl);
                    Region acRegion1 = myRegionColl[0] as Region;
                    Region acRegion2 = myRegionColl[1] as Region;
    
                    // Subtract region 1 from region 2
                    if (acRegion1.Area > acRegion2.Area)
                    {
                        // Subtract the smaller region from the larger one
                        acRegion1.BooleanOperation(BooleanOperationType.BoolSubtract, acRegion2);
                        acRegion2.Dispose();
    
                        // Add the final region to the database
                        acBlkTblRec.AppendEntity(acRegion1);
                        acTrans.AddNewlyCreatedDBObject(acRegion1, true);
                    }
                    else
                    {
                        // Subtract the smaller region from the larger one
                        acRegion2.BooleanOperation(BooleanOperationType.BoolSubtract, acRegion1);
                        acRegion1.Dispose();
    
                        // Add the final region to the database
                        acBlkTblRec.AppendEntity(acRegion2);
                        acTrans.AddNewlyCreatedDBObject(acRegion2, true);
                    }
    
                    // Dispose of the in memory objects not appended to the database
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreateCompositeRegions")> _
    Public Sub CreateCompositeRegions()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create two in memory circles
            Using acCirc1 As Circle = New Circle()
                acCirc1.Center = New Point3d(4, 4, 0)
                acCirc1.Radius = 2
    
                Using acCirc2 As Circle = New Circle()
                    acCirc2.Center = New Point3d(4, 4, 0)
                    acCirc2.Radius = 1
    
                    '' Adds the circle to an object array
                    Dim acDBObjColl As DBObjectCollection = New DBObjectCollection()
                    acDBObjColl.Add(acCirc1)
                    acDBObjColl.Add(acCirc2)
    
                    '' Calculate the regions based on each closed loop
                    Dim myRegionColl As DBObjectCollection = New DBObjectCollection()
                    myRegionColl = Region.CreateFromCurves(acDBObjColl)
                    Dim acRegion1 As Region = myRegionColl(0)
                    Dim acRegion2 As Region = myRegionColl(1)
    
                    '' Subtract region 1 from region 2
                    If acRegion1.Area > acRegion2.Area Then
                        '' Subtract the smaller region from the larger one
                        acRegion1.BooleanOperation(BooleanOperationType.BoolSubtract, acRegion2)
                        acRegion2.Dispose()
    
                        '' Add the final region to the database
                        acBlkTblRec.AppendEntity(acRegion1)
                        acTrans.AddNewlyCreatedDBObject(acRegion1, True)
                    Else
                        '' Subtract the smaller region from the larger one
                        acRegion2.BooleanOperation(BooleanOperationType.BoolSubtract, acRegion1)
                        acRegion1.Dispose()
    
                        '' Add the final region to the database
                        acBlkTblRec.AppendEntity(acRegion2)
                        acTrans.AddNewlyCreatedDBObject(acRegion2, True)
                    End If
    
                    '' Dispose of the in memory objects not appended to the database
                End Using
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateCompositeRegions()
        ' Create two circles, one representing outside of the wheel,
        ' the other the center of the wheel
        Dim DonutParts(0 To 1) As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 4
        center(1) = 4
        center(2) = 0
        radius = 2#
        Set WheelParts(0) = ThisDrawing.ModelSpace. _
                                AddCircle(center, radius)
        radius = 1#
        Set WheelParts(1) = ThisDrawing.ModelSpace. _
                                AddCircle(center, radius)
     
        ' Create a region from the two circles
        Dim regions As Variant
        regions = ThisDrawing.ModelSpace.AddRegion(WheelParts)
     
        ' Copy the regions into the region variables for ease of use
        Dim WheelOuter As AcadRegion
        Dim WheelInner As AcadRegion
     
        If regions(0).Area > regions(1).Area Then
            ' The first region is the outer edge of the wheel
            Set WheelOuter = regions(0)
            Set WheelInner = regions(1)
        Else
            ' The first region is the inner edge of the wheel
            Set WheelInner = regions(0)
            Set WheelOuter = regions(1)
        End If
     
        ' Subtract the smaller circle from the larger circle
        WheelOuter.Boolean acSubtraction, WheelInner
    End Sub
