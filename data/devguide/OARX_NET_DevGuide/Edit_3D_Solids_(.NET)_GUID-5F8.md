<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Edit 3D Solids (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-5F8D4718-D0A5-41F9-9178-A4508133855A.htm -->

# Edit 3D Solids (.NET)

Once you have created a solid, you can create more complex shapes by combining or subtracting solids. You can join solids, subtract solids from each other, or find the common volume (overlapping portion) of solids. Use the BooleanOperation method to perform these combinations. The CheckInterference method allows you to determine if two solids overlap. 

Solids are further modified by obtaining the 2D cross section of a solid or slicing a solid into two pieces. Use the GetSection method to find cross sections of solids, and the Slice method for slicing a solid into two pieces. 

## Find the interference between two solids

This example creates a box and cylinder. It then finds the interference between the two solids and creates a new solid from that interference. For ease of viewing, the box is colored white, the cylinder is colored cyan, and the interference solid is colored red. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("FindInterferenceBetweenSolids")]
    public static void FindInterferenceBetweenSolids()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table record for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                            OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a 3D solid box
            using (Solid3d acSol3DBox = new Solid3d())
            {
                acSol3DBox.CreateBox(5, 7, 10);
                acSol3DBox.ColorIndex = 7;
    
                // Position the center of the 3D solid at (5,5,0) 
                acSol3DBox.TransformBy(Matrix3d.Displacement(new Point3d(5, 5, 0) -
                                                                Point3d.Origin));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DBox);
                acTrans.AddNewlyCreatedDBObject(acSol3DBox, true);
    
                // Create a 3D solid cylinder
                // 3D solids are created at (0,0,0) so there is no need to move it
                using (Solid3d acSol3DCyl = new Solid3d())
                {
                    acSol3DCyl.CreateFrustum(20, 5, 5, 5);
                    acSol3DCyl.ColorIndex = 4;
    
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acSol3DCyl);
                    acTrans.AddNewlyCreatedDBObject(acSol3DCyl, true);
    
                    // Create a 3D solid from the interference of the box and cylinder
                    Solid3d acSol3DCopy = acSol3DCyl.Clone() as Solid3d;
    
                    // Check to see if the 3D solids overlap
                    if (acSol3DCopy.CheckInterference(acSol3DBox) == true)
                    {
                        acSol3DCopy.BooleanOperation(BooleanOperationType.BoolIntersect,
                                                        acSol3DBox.Clone() as Solid3d);
    
                        acSol3DCopy.ColorIndex = 1;
                    }
    
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acSol3DCopy);
                    acTrans.AddNewlyCreatedDBObject(acSol3DCopy, true);
                }
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
     
    <CommandMethod("FindInterferenceBetweenSolids")> _
    Public Sub FindInterferenceBetweenSolids()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a 3D solid box
            Using acSol3DBox As Solid3d = New Solid3d()
                acSol3DBox.CreateBox(5, 7, 10)
                acSol3DBox.ColorIndex = 7
    
                '' Position the center of the 3D solid at (5,5,0) 
                acSol3DBox.TransformBy(Matrix3d.Displacement(New Point3d(5, 5, 0) - _
                                                             Point3d.Origin))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DBox)
                acTrans.AddNewlyCreatedDBObject(acSol3DBox, True)
    
                '' Create a 3D solid cylinder
                '' 3D solids are created at (0,0,0) so there is no need to move it
                Using acSol3DCyl As Solid3d = New Solid3d()
                    acSol3DCyl.CreateFrustum(20, 5, 5, 5)
                    acSol3DCyl.ColorIndex = 4
    
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acSol3DCyl)
                    acTrans.AddNewlyCreatedDBObject(acSol3DCyl, True)
    
                    '' Create a 3D solid from the interference of the box and cylinder
                    Dim acSol3DCopy As Solid3d = acSol3DCyl.Clone()
    
                    '' Check to see if the 3D solids overlap
                    If acSol3DCopy.CheckInterference(acSol3DBox) = True Then
                        acSol3DCopy.BooleanOperation(BooleanOperationType.BoolIntersect, _
                                                     acSol3DBox.Clone())
    
                        acSol3DCopy.ColorIndex = 1
                    End If
    
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acSol3DCopy)
                    acTrans.AddNewlyCreatedDBObject(acSol3DCopy, True)
                End Using
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FindInterferenceBetweenSolids()
        ' Define the box
        Dim boxObj As Acad3DSolid
        Dim length As Double
        Dim width As Double
        Dim height As Double
        Dim center(0 To 2) As Double
        center(0) = 5: center(1) = 5: center(2) = 0
        length = 5
        width = 7
        height = 10
     
        ' Create the box object in model space
        ' and color it white
        Set boxObj = ThisDrawing.ModelSpace. _
                         AddBox(center, length, width, height)
        boxObj.Color = acWhite
     
        ' Define the cylinder
        Dim cylinderObj As Acad3DSolid
        Dim cylinderRadius As Double
        Dim cylinderHeight As Double
        center(0) = 0: center(1) = 0: center(2) = 0
        cylinderRadius = 5
        cylinderHeight = 20
     
        ' Create the Cylinder and
        ' color it cyan
        Set cylinderObj = ThisDrawing.ModelSpace. _
                              AddCylinder(center, cylinderRadius, cylinderHeight)
        cylinderObj.Color = acCyan
     
        ' Find the interference between the two solids
        ' and create a new solid from it. Color the
        ' new solid red.
        Dim solidObj As Acad3DSolid
        Set solidObj = boxObj.CheckInterference(cylinderObj, True)
        solidObj.Color = acRed
     
        ZoomAll
    End Sub

## Slice a solid into two solids

This example creates a box in model space. It then slices the box based on a plane defined by three points. The slice is returned as a 3DSolid. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("SliceABox")]
    public static void SliceABox()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table record for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                            OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a 3D solid box
            using (Solid3d acSol3D = new Solid3d())
            {
                acSol3D.CreateBox(5, 7, 10);
                acSol3D.ColorIndex = 7;
    
                // Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(new Point3d(5, 5, 0) -
                                                            Point3d.Origin));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D);
                acTrans.AddNewlyCreatedDBObject(acSol3D, true);
    
                // Define the mirror plane
                Plane acPlane = new Plane(new Point3d(1.5, 7.5, 0),
                                            new Point3d(1.5, 7.5, 10),
                                            new Point3d(8.5, 2.5, 10));
    
                Solid3d acSol3DSlice = acSol3D.Slice(acPlane, true);
                acSol3DSlice.ColorIndex = 1;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DSlice);
                acTrans.AddNewlyCreatedDBObject(acSol3DSlice, true);
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
     
    <CommandMethod("SliceABox")> _
    Public Sub SliceABox()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a 3D solid box
            Using acSol3D As Solid3d = New Solid3d()
                acSol3D.CreateBox(5, 7, 10)
                acSol3D.ColorIndex = 7
    
                '' Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(New Point3d(5, 5, 0) - _
                                                          Point3d.Origin))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D)
                acTrans.AddNewlyCreatedDBObject(acSol3D, True)
    
                '' Define the mirror plane
                Dim acPlane As Plane = New Plane(New Point3d(1.5, 7.5, 0), _
                                       New Point3d(1.5, 7.5, 10), _
                                       New Point3d(8.5, 2.5, 10))
    
                Dim acSol3DSlice As Solid3d = acSol3D.Slice(acPlane, True)
                acSol3DSlice.ColorIndex = 1
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DSlice)
                acTrans.AddNewlyCreatedDBObject(acSol3DSlice, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SliceABox()
        ' Create the box object
        Dim boxObj As Acad3DSolid
        Dim length As Double
        Dim width As Double
        Dim height As Double
        Dim center(0 To 2) As Double
        center(0) = 5#: center(1) = 5#: center(2) = 0
        length = 5#: width = 7: height = 10#
     
        ' Create the box (3DSolid) object in model space
        Set boxObj = ThisDrawing.ModelSpace. _
                         AddBox(center, length, width, height)
        boxObj.Color = acWhite
     
        ' Define the section plane with three points
        Dim slicePt1(0 To 2) As Double
        Dim slicePt2(0 To 2) As Double
        Dim slicePt3(0 To 2) As Double
     
        slicePt1(0) = 1.5: slicePt1(1) = 7.5: slicePt1(2) = 0
        slicePt2(0) = 1.5: slicePt2(1) = 7.5: slicePt2(2) = 10
        slicePt3(0) = 8.5: slicePt3(1) = 2.5: slicePt3(2) = 10
     
        ' slice the box and color the new solid red
        Dim sliceObj As Acad3DSolid
        Set sliceObj = boxObj.SliceSolid _
                              (slicePt1, slicePt2, slicePt3, True)
        sliceObj.Color = acRed
     
        ZoomAll
    End Sub
