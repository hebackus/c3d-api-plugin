<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Create 3D Objects (.NET) > Create Meshes (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C86C734C-ABA8-436A-B383-DA0A4B562267.htm -->

# Create Meshes (.NET)

A rectangular mesh (PolygonMesh object) represents the surface of an object using planar facets. The density or number of facets for a mesh is defined in terms of a matrix of _M_ and _N_ vertices, similar to a grid consisting of columns and rows. _M_ and _N_ specify the column and row position, respectively, of any given vertex. You can create meshes in both 2D and 3D, but they are used primarily for 3D. 

Create an instance of a PolygonMesh object and then specify the density and placement of the vertices for the new mesh. This method optionally takes six values: the type of Polygon Mesh to create, two integers that define the number of vertices in the _M_ and _N_ directions, a collection of points containing the coordinates for all the vertices in the mesh, and two booleans that define if the mesh is closed in the _M_ or _N_ directions. 

Once the PolygonMesh is created, use the IsMClosed and NClosed properties to close the mesh. 

## Create a polygon mesh

This example creates a 4×4 polygon mesh. The direction of the active viewport is then adjusted so that the three-dimensional nature of the mesh is more easily viewed. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("Create3DMesh")]
    public static void Create3DMesh()
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
    
            // Create a polygon mesh
            using (PolygonMesh acPolyMesh = new PolygonMesh())
            {
                acPolyMesh.MSize = 4;
                acPolyMesh.NSize = 4;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPolyMesh);
                acTrans.AddNewlyCreatedDBObject(acPolyMesh, true);
    
                // Before adding vertexes, the polyline must be in the drawing
                Point3dCollection acPts3dPMesh = new Point3dCollection();
                acPts3dPMesh.Add(new Point3d(0, 0, 0));
                acPts3dPMesh.Add(new Point3d(2, 0, 1));
                acPts3dPMesh.Add(new Point3d(4, 0, 0));
                acPts3dPMesh.Add(new Point3d(6, 0, 1));
    
                acPts3dPMesh.Add(new Point3d(0, 2, 0));
                acPts3dPMesh.Add(new Point3d(2, 2, 1));
                acPts3dPMesh.Add(new Point3d(4, 2, 0));
                acPts3dPMesh.Add(new Point3d(6, 2, 1));
    
                acPts3dPMesh.Add(new Point3d(0, 4, 0));
                acPts3dPMesh.Add(new Point3d(2, 4, 1));
                acPts3dPMesh.Add(new Point3d(4, 4, 0));
                acPts3dPMesh.Add(new Point3d(6, 4, 0));
    
                acPts3dPMesh.Add(new Point3d(0, 6, 0));
                acPts3dPMesh.Add(new Point3d(2, 6, 1));
                acPts3dPMesh.Add(new Point3d(4, 6, 0));
                acPts3dPMesh.Add(new Point3d(6, 6, 0));
    
                foreach (Point3d acPt3d in acPts3dPMesh)
                {
                    PolygonMeshVertex acPMeshVer = new PolygonMeshVertex(acPt3d);
                    acPolyMesh.AppendVertex(acPMeshVer);
                    acTrans.AddNewlyCreatedDBObject(acPMeshVer, true);
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
     
    <CommandMethod("Create3DMesh")> _
    Public Sub Create3DMesh()
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
    
            '' Create a polygon mesh
            Using acPolyMesh As PolygonMesh = New PolygonMesh()
                acPolyMesh.MSize = 4
                acPolyMesh.NSize = 4
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPolyMesh)
                acTrans.AddNewlyCreatedDBObject(acPolyMesh, True)
    
                '' Before adding vertexes, the polyline must be in the drawing
                Dim acPts3dPMesh As Point3dCollection = New Point3dCollection()
                acPts3dPMesh.Add(New Point3d(0, 0, 0))
                acPts3dPMesh.Add(New Point3d(2, 0, 1))
                acPts3dPMesh.Add(New Point3d(4, 0, 0))
                acPts3dPMesh.Add(New Point3d(6, 0, 1))
    
                acPts3dPMesh.Add(New Point3d(0, 2, 0))
                acPts3dPMesh.Add(New Point3d(2, 2, 1))
                acPts3dPMesh.Add(New Point3d(4, 2, 0))
                acPts3dPMesh.Add(New Point3d(6, 2, 1))
    
                acPts3dPMesh.Add(New Point3d(0, 4, 0))
                acPts3dPMesh.Add(New Point3d(2, 4, 1))
                acPts3dPMesh.Add(New Point3d(4, 4, 0))
                acPts3dPMesh.Add(New Point3d(6, 4, 0))
    
                acPts3dPMesh.Add(New Point3d(0, 6, 0))
                acPts3dPMesh.Add(New Point3d(2, 6, 1))
                acPts3dPMesh.Add(New Point3d(4, 6, 0))
                acPts3dPMesh.Add(New Point3d(6, 6, 0))
    
                For Each acPt3d As Point3d In acPts3dPMesh
                    Dim acPMeshVer As PolygonMeshVertex = New PolygonMeshVertex(acPt3d)
                    acPolyMesh.AppendVertex(acPMeshVer)
                    acTrans.AddNewlyCreatedDBObject(acPMeshVer, True)
                Next
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
    
    
    Sub Create3DMesh()
        Dim meshObj As AcadPolygonMesh
        Dim mSize, nSize, Count As Integer
     
        ' create the matrix of points
        Dim points(0 To 47) As Double
        points(0) = 0: points(1) = 0: points(2) = 0
        points(3) = 2: points(4) = 0: points(5) = 1
        points(6) = 4: points(7) = 0: points(8) = 0
        points(9) = 6: points(10) = 0: points(11) = 1
        points(12) = 0: points(13) = 2: points(14) = 0
        points(15) = 2: points(16) = 2: points(17) = 1
        points(18) = 4: points(19) = 2: points(20) = 0
        points(21) = 6: points(22) = 2: points(23) = 1
        points(24) = 0: points(25) = 4: points(26) = 0
        points(27) = 2: points(28) = 4: points(29) = 1
        points(30) = 4: points(31) = 4: points(32) = 0
        points(33) = 6: points(34) = 4: points(35) = 0
        points(36) = 0: points(37) = 6: points(38) = 0
        points(39) = 2: points(40) = 6: points(41) = 1
        points(42) = 4: points(43) = 6: points(44) = 0
        points(45) = 6: points(46) = 6: points(47) = 0
     
        mSize = 4: nSize = 4
     
        ' creates a 3Dmesh in model space
        Set meshObj = ThisDrawing.ModelSpace. _
                          Add3DMesh(mSize, nSize, points)
     
        ' Change the viewing direction of the viewport
        ' to better see the cylinder
        Dim NewDirection(0 To 2) As Double
        NewDirection(0) = -1
        NewDirection(1) = -1
        NewDirection(2) = 1
        ThisDrawing.ActiveViewport.direction = NewDirection
        ThisDrawing.ActiveViewport = ThisDrawing.ActiveViewport
     
        ZoomAll
    End Sub
