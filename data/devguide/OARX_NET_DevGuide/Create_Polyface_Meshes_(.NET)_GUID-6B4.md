<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Create 3D Objects (.NET) > Create Polyface Meshes (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6B49EE98-D513-46EB-9D7A-282F70A45B24.htm -->

# Create Polyface Meshes (.NET)

A polyface mesh represents the surface of an object defined by faces capable of having numerous vertices. Creating a polyface mesh is similar to creating a rectangular mesh. You create a polyface mesh by creating an instance of a PolyFaceMesh object. The constructor of the PolyFaceMesh object does not accept any parameters. To add a vertex to a polyface mesh, you create a PolyFaceMeshVertex and add it to the PolyFaceMesh object using the AppendVertex method. 

As you create the polyface mesh, you can set specific edges to be invisible, assign them to layers, or give them colors. To make an edge invisible, you create an instance of a FaceRecord and set which edges should be invisible and then append the FaceRecord object to the PolyFaceMesh object using the AppendFaceRecord method. 

## Create a polyface mesh

This example creates a PolyfaceMesh object and changes the viewing direction of the active viewport to display the three-dimensional nature of the mesh. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreatePolyfaceMesh")]
    public static void CreatePolyfaceMesh()
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
    
            // Create a polyface mesh
            using (PolyFaceMesh acPFaceMesh = new PolyFaceMesh())
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPFaceMesh);
                acTrans.AddNewlyCreatedDBObject(acPFaceMesh, true);
    
                // Before adding vertexes, the polyline must be in the drawing
                Point3dCollection acPts3dPFMesh = new Point3dCollection();
                acPts3dPFMesh.Add(new Point3d(4, 7, 0));
                acPts3dPFMesh.Add(new Point3d(5, 7, 0));
                acPts3dPFMesh.Add(new Point3d(6, 7, 0));
    
                acPts3dPFMesh.Add(new Point3d(4, 6, 0));
                acPts3dPFMesh.Add(new Point3d(5, 6, 0));
                acPts3dPFMesh.Add(new Point3d(6, 6, 1));
    
                foreach (Point3d acPt3d in acPts3dPFMesh)
                {
                    PolyFaceMeshVertex acPMeshVer = new PolyFaceMeshVertex(acPt3d);
                    acPFaceMesh.AppendVertex(acPMeshVer);
                    acTrans.AddNewlyCreatedDBObject(acPMeshVer, true);
                }
    
                using (FaceRecord acFaceRec1 = new FaceRecord(1, 2, 5, 4))
                {
                    acPFaceMesh.AppendFaceRecord(acFaceRec1);
                    acTrans.AddNewlyCreatedDBObject(acFaceRec1, true);
                }
    
                using (FaceRecord acFaceRec2 = new FaceRecord(2, 3, 6, 5))
                {
                    acPFaceMesh.AppendFaceRecord(acFaceRec2);
                    acTrans.AddNewlyCreatedDBObject(acFaceRec2, true);
                }
            }
    
            // Open the active viewport
            ViewportTableRecord acVportTblRec;
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId,
                                                OpenMode.ForWrite) as ViewportTableRecord;
    
            // Rotate the view direction of the current viewport
            acVportTblRec.ViewDirection = new Vector3d(-1, -1, 1);
            acDoc.Editor.UpdateTiledViewportsFromDatabase();
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreatePolyfaceMesh")> _
    Public Sub CreatePolyfaceMesh()
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
    
            '' Create a polyface mesh
            Using acPFaceMesh As PolyFaceMesh = New PolyFaceMesh()
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPFaceMesh)
                acTrans.AddNewlyCreatedDBObject(acPFaceMesh, True)
    
                '' Before adding vertexes, the polyline must be in the drawing
                Dim acPts3dPFMesh As Point3dCollection = New Point3dCollection()
                acPts3dPFMesh.Add(New Point3d(4, 7, 0))
                acPts3dPFMesh.Add(New Point3d(5, 7, 0))
                acPts3dPFMesh.Add(New Point3d(6, 7, 0))
    
                acPts3dPFMesh.Add(New Point3d(4, 6, 0))
                acPts3dPFMesh.Add(New Point3d(5, 6, 0))
                acPts3dPFMesh.Add(New Point3d(6, 6, 1))
    
                For Each acPt3d As Point3d In acPts3dPFMesh
                    Dim acPMeshVer As PolyFaceMeshVertex = New PolyFaceMeshVertex(acPt3d)
                    acPFaceMesh.AppendVertex(acPMeshVer)
                    acTrans.AddNewlyCreatedDBObject(acPMeshVer, True)
                Next
    
                Using acFaceRec1 As FaceRecord = New FaceRecord(1, 2, 5, 4)
                    acPFaceMesh.AppendFaceRecord(acFaceRec1)
                    acTrans.AddNewlyCreatedDBObject(acFaceRec1, True)
                End Using
    
                Using acFaceRec2 As FaceRecord = New FaceRecord(2, 3, 6, 5)
                    acPFaceMesh.AppendFaceRecord(acFaceRec2)
                    acTrans.AddNewlyCreatedDBObject(acFaceRec2, True)
                End Using
            End Using
    
            '' Open the active viewport
            Dim acVportTblRec As ViewportTableRecord
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId, _
                                              OpenMode.ForWrite)
    
            '' Rotate the view direction of the current viewport
            acVportTblRec.ViewDirection = New Vector3d(-1, -1, 1)
            acDoc.Editor.UpdateTiledViewportsFromDatabase()
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreatePolyfaceMesh()
        'Define the mesh vertices
        Dim vertex(0 To 17) As Double
        vertex(0) = 4: vertex(1) = 7: vertex(2) = 0
        vertex(3) = 5: vertex(4) = 7: vertex(5) = 0
        vertex(6) = 6: vertex(7) = 7: vertex(8) = 0
        vertex(9) = 4: vertex(10) = 6: vertex(11) = 0
        vertex(12) = 5: vertex(13) = 6: vertex(14) = 0
        vertex(15) = 6: vertex(16) = 6: vertex(17) = 1
     
        ' Define the face list
        Dim FaceList(0 To 7) As Integer
        FaceList(0) = 1
        FaceList(1) = 2
        FaceList(2) = 5
        FaceList(3) = 4
        FaceList(4) = 2
        FaceList(5) = 3
        FaceList(6) = 6
        FaceList(7) = 5
     
        ' Create the polyface mesh
        Dim polyfaceMeshObj As AcadPolyfaceMesh
        Set polyfaceMeshObj = ThisDrawing.ModelSpace. _
                                  AddPolyfaceMesh(vertex, FaceList)
     
        ' Change the viewing direction of the viewport to
        ' better see the polyface mesh
        Dim NewDirection(0 To 2) As Double
        NewDirection(0) = -1
        NewDirection(1) = -1
        NewDirection(2) = 1
        ThisDrawing.ActiveViewport.direction = NewDirection
        ThisDrawing.ActiveViewport = ThisDrawing.ActiveViewport
     
        ZoomAll
    End Sub
