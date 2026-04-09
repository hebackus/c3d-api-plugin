<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Explode Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E8262AC4-6A6B-4D9A-8AC6-C12ED6F72ED1.htm -->

# Explode Objects (.NET)

Exploding an object converts the single object to its constituent parts. You use the Explode function to explode an object, and it requires a DBObjectCollection object in which is used to return the resulting objects. For example, exploding a polyline can result in the creation of an object collection that contains multiple lines and arcs. 

If a block is exploded, the object collection returned holds the graphical objects in which define the block. After an object is exploded, the original object is left unaltered. If you want the returned objects to replace the original object, the original object must be erased and then the returned objects must be added to a block table record. 

## Explode a polyline

This example creates a lightweight polyline object and then explodes the polyline into its simplest objects. After the polyline is exploded, it is disposed of and the returned objects are added to Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("ExplodeObject")]
    public static void ExplodeObject()
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
    
            // Create a lightweight polyline
            using (Polyline acPoly = new Polyline())
            {
                acPoly.AddVertexAt(0, new Point2d(1, 1), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(1, 2), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(2, 2), 0, 0, 0);
                acPoly.AddVertexAt(3, new Point2d(3, 2), 0, 0, 0);
                acPoly.AddVertexAt(4, new Point2d(4, 4), 0, 0, 0);
                acPoly.AddVertexAt(5, new Point2d(4, 1), 0, 0, 0);
    
                // Sets the bulge at index 3
                acPoly.SetBulgeAt(3, -0.5);
    
                // Explodes the polyline
                DBObjectCollection acDBObjColl = new DBObjectCollection();
                acPoly.Explode(acDBObjColl);
    
                foreach (Entity acEnt in acDBObjColl)
                {
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acEnt);
                    acTrans.AddNewlyCreatedDBObject(acEnt, true);
                }
    
                // Dispose of the in memory polyline
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("ExplodeObject")> _
    Public Sub ExplodeObject()
        '' Get the current document and database
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
    
            '' Create a lightweight polyline
            Using acPoly As Polyline = New Polyline()
                acPoly.AddVertexAt(0, New Point2d(1, 1), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(1, 2), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(2, 2), 0, 0, 0)
                acPoly.AddVertexAt(3, New Point2d(3, 2), 0, 0, 0)
                acPoly.AddVertexAt(4, New Point2d(4, 4), 0, 0, 0)
                acPoly.AddVertexAt(5, New Point2d(4, 1), 0, 0, 0)
    
                '' Sets the bulge at index 3
                acPoly.SetBulgeAt(3, -0.5)
    
                '' Explodes the polyline
                Dim acDBObjColl As DBObjectCollection = New DBObjectCollection()
                acPoly.Explode(acDBObjColl)
    
                For Each acEnt As Entity In acDBObjColl
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acEnt)
                    acTrans.AddNewlyCreatedDBObject(acEnt, True)
                Next
    
                '' Dispose of the in memory polyline
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ExplodeObject()
        Dim plineObj As AcadLWPolyline
        Dim points(0 To 11) As Double
     
        ' Define the 2D polyline points
        points(0) = 1: points(1) = 1
        points(2) = 1: points(3) = 2
        points(4) = 2: points(5) = 2
        points(6) = 3: points(7) = 2
        points(8) = 4: points(9) = 4
        points(10) = 4: points(11) = 1
     
        ' Create a light weight Polyline object
        Set plineObj = ThisDrawing.ModelSpace. _
                                     AddLightWeightPolyline(points)
     
        ' Set the bulge on one segment to vary the
        ' type of objects in the polyline
        plineObj.SetBulge 3, -0.5
     
        ' Explode the polyline
        Dim explodedObjects As Variant
        explodedObjects = plineObj.Explode
     
        ' Erase the polyline
        plineObj.Erase
    End Sub
