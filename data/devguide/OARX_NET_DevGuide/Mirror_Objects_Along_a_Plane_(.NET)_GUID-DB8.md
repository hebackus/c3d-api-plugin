<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Edit in 3D (.NET) > Mirror Objects Along a Plane (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DB878847-8F95-4E82-AF2A-304236B86D0E.htm -->

# Mirror Objects Along a Plane (.NET)

With the TransformBy method of an object and the Mirroring method of a Matrix, you can mirror objects along a specified mirroring plane specified by three points. 

## Mirror in 3D

This example creates a box in model space. It then mirrors the box about a plane and colors the mirrored box red. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("MirrorABox3D")]
    public static void MirrorABox3D()
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
    
                // Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(new Point3d(5, 5, 0) -
                                                            Point3d.Origin));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D);
                acTrans.AddNewlyCreatedDBObject(acSol3D, true);
    
                // Create a copy of the original 3D solid and change the color of the copy
                Solid3d acSol3DCopy = acSol3D.Clone() as Solid3d;
                acSol3DCopy.ColorIndex = 1;
    
                // Define the mirror plane
                Plane acPlane = new Plane(new Point3d(1.25, 0, 0),
                                            new Point3d(1.25, 2, 0),
                                            new Point3d(1.25, 2, 2));
    
                // Mirror the 3D solid across the plane
                acSol3DCopy.TransformBy(Matrix3d.Mirroring(acPlane));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DCopy);
                acTrans.AddNewlyCreatedDBObject(acSol3DCopy, true);
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
     
    <CommandMethod("MirrorABox3D")> _
    Public Sub MirrorABox3D()
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
    
                '' Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(New Point3d(5, 5, 0) - _
                                                          Point3d.Origin))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D)
                acTrans.AddNewlyCreatedDBObject(acSol3D, True)
    
                '' Create a copy of the original 3D solid and change the color of the copy
                Dim acSol3DCopy As Solid3d = acSol3D.Clone()
                acSol3DCopy.ColorIndex = 1
    
                '' Define the mirror plane
                Dim acPlane As Plane = New Plane(New Point3d(1.25, 0, 0), _
                                                 New Point3d(1.25, 2, 0), _
                                                 New Point3d(1.25, 2, 2))
    
                '' Mirror the 3D solid across the plane
                acSol3DCopy.TransformBy(Matrix3d.Mirroring(acPlane))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3DCopy)
                acTrans.AddNewlyCreatedDBObject(acSol3DCopy, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MirrorABox3D()
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
     
        ' Define the mirroring plane with three points
        Dim mirrorPt1(0 To 2) As Double
        Dim mirrorPt2(0 To 2) As Double
        Dim mirrorPt3(0 To 2) As Double
     
        mirrorPt1(0) = 1.25: mirrorPt1(1) = 0: mirrorPt1(2) = 0
        mirrorPt2(0) = 1.25: mirrorPt2(1) = 2: mirrorPt2(2) = 0
        mirrorPt3(0) = 1.25: mirrorPt3(1) = 2: mirrorPt3(2) = 2
     
        ' Mirror the box
        Dim mirrorBoxObj As Acad3DSolid
        Set mirrorBoxObj = boxObj.Mirror3D _
                              (mirrorPt1, mirrorPt2, mirrorPt3)
        mirrorBoxObj.Color = acRed
     
        ZoomAll
    End Sub
