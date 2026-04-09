<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Work With Regions (.NET) > Create Regions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9CD22AE5-8F66-4925-A155-95852BAFD565.htm -->

# Create Regions (.NET)

Regions are added to a BlockTableRecord object by creating an instance of a Region object and then appending it to a BlockTableRecord. Before you can add it to a BlockTableRecord object, a region needs to be calculated based on the objects that form the closed loop. The CreateFromCurves function creates a region out of every closed loop formed by the input array of objects. The CreateFromCurves method returns and requires a DBObjectCollection object. 

AutoCAD converts closed 2D and planar 3D polylines to separate regions, then converts polylines, lines, and curves that form closed planar loops. If more than two curves share an endpoint, the resulting region might be arbitrary. Because of this, several regions may actually be created with the CreateFromCurves method. You need to append each region created to a BlockTableRecord object. 

## Create a simple region 

The following example creates a region from a single circle. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddRegion")]
    public static void AddRegion()
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
    
            // Create an in memory circle
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 5;
    
                // Adds the circle to an object array
                DBObjectCollection acDBObjColl = new DBObjectCollection();
                acDBObjColl.Add(acCirc);
    
                // Calculate the regions based on each closed loop
                DBObjectCollection myRegionColl = new DBObjectCollection();
                myRegionColl = Region.CreateFromCurves(acDBObjColl);
                Region acRegion = myRegionColl[0] as Region;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acRegion);
                acTrans.AddNewlyCreatedDBObject(acRegion, true);
    
                // Dispose of the in memory circle not appended to the database
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
     
    <CommandMethod("AddRegion")> _
    Public Sub AddRegion()
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
    
            '' Create an in memory circle
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 5
    
                '' Adds the circle to an object array
                Dim acDBObjColl As DBObjectCollection = New DBObjectCollection()
                acDBObjColl.Add(acCirc)
    
                '' Calculate the regions based on each closed loop
                Dim myRegionColl As DBObjectCollection = New DBObjectCollection()
                myRegionColl = Region.CreateFromCurves(acDBObjColl)
                Dim acRegion As Region = myRegionColl(0)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acRegion)
                acTrans.AddNewlyCreatedDBObject(acRegion, True)
    
                '' Dispose of the in memory object not appended to the database
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddRegion()
        ' Define an array to hold the
        ' boundaries of the region.
        Dim curves(0 To 0) As AcadCircle
     
        ' Create a circle to become a
        ' boundary for the region.
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2
        center(1) = 2
        center(2) = 0
        radius = 5#
        Set curves(0) = ThisDrawing.ModelSpace.AddCircle _
                                         (center, radius)
     
        ' Create the region
        Dim regionObj As Variant
        regionObj = ThisDrawing.ModelSpace.AddRegion(curves)
     
        ZoomAll
    End Sub
