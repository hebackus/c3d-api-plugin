<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Solid-Filled Areas (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-0544EA65-BA88-4BC5-99F4-D9FAF7BE9FE9.htm -->

# Create Solid-Filled Areas (.NET)

You can create triangular and quadrilateral areas filled with a color. When creating filled areas, set the FILLMODE system variable to off to improve performance and back on once the fills have been created. 

When you create a quadrilateral solid-filled area, the sequence of the third and fourth points determines its shape. Compare the following illustrations: 

The first two points define one edge of the polygon. The third point is defined diagonally opposite from the second. If the fourth point is set equal to the third point, then a filled triangle is created. 

## Create a solid-filled object

The following example creates a quadrilateral solid (bow-tie) in Model space using the coordinates (0, 0, 0), (5, 0, 0), (5, 8, 0), and (0, 8, 0). It also creates a quadrilateral solid in a rectangular shape using the coordinates (10, 0, 0), (15, 0, 0), (10, 8, 0), and (15, 8, 0). 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("Add2DSolid")]
    public static void Add2DSolid()
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
    
            // Create a quadrilateral (bow-tie) solid in Model space
            using (Solid ac2DSolidBow = new Solid(new Point3d(0, 0, 0),
                                            new Point3d(5, 0, 0),
                                            new Point3d(5, 8, 0),
                                            new Point3d(0, 8, 0)))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(ac2DSolidBow);
                acTrans.AddNewlyCreatedDBObject(ac2DSolidBow, true);
            }
    
            // Create a quadrilateral (square) solid in Model space
            using (Solid ac2DSolidSqr = new Solid(new Point3d(10, 0, 0),
                                            new Point3d(15, 0, 0),
                                            new Point3d(10, 8, 0),
                                            new Point3d(15, 8, 0)))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(ac2DSolidSqr);
                acTrans.AddNewlyCreatedDBObject(ac2DSolidSqr, true);
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
     
    <CommandMethod("Add2DSolid")> _
    Public Sub Add2DSolid()
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
    
            '' Create a quadrilateral (bow-tie) solid in Model space
            Using ac2DSolidBow As Solid = New Solid(New Point3d(0, 0, 0), _
                                                    New Point3d(5, 0, 0), _
                                                    New Point3d(5, 8, 0), _
                                                    New Point3d(0, 8, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(ac2DSolidBow)
                acTrans.AddNewlyCreatedDBObject(ac2DSolidBow, True)
            End Using
    
            '' Create a quadrilateral (square) solid in Model space
            Using ac2DSolidSqr As Solid = New Solid(New Point3d(10, 0, 0), _
                                                    New Point3d(15, 0, 0), _
                                                    New Point3d(10, 8, 0), _
                                                    New Point3d(15, 8, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(ac2DSolidSqr)
                acTrans.AddNewlyCreatedDBObject(ac2DSolidSqr, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub Add2DSolid()
        Dim solidObj As AcadSolid
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
        Dim point3(0 To 2) As Double
        Dim point4(0 To 2) As Double
     
        ' Define the solid
        point1(0) = 0#: point1(1) = 0#: point1(2) = 0#
        point2(0) = 5#: point2(1) = 0#: point2(2) = 0#
        point3(0) = 5#: point3(1) = 8#: point3(2) = 0#
        point4(0) = 0#: point4(1) = 8#: point4(2) = 0#
        ' Create the solid object in model space
        Set solidObj = ThisDrawing.ModelSpace.AddSolid _
                                        (point1, point2, point3, point4)
     
        ' Define the solid
        point1(0) = 10#: point1(1) = 0#: point1(2) = 0#
        point2(0) = 15#: point2(1) = 0#: point2(2) = 0#
        point3(0) = 10#: point3(1) = 8#: point3(2) = 0#
        point4(0) = 15#: point4(1) = 8#: point4(2) = 0#
        ' Create the solid object in model space
        Set solidObj = ThisDrawing.ModelSpace.AddSolid _
                                        (point1, point2, point3, point4)
     
        ZoomAll
    End Sub
