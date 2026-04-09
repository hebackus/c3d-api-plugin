<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Create 3D Objects (.NET) > Create Solids (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A5DEE210-347C-4FB7-A0D7-C48F3B949225.htm -->

# Create Solids (.NET)

A solid object (Solid3d object) represents the entire volume of an object. Solids are the most informationally complete and least ambiguous of the 3D modeling types. Complex solid shapes are also easier to construct and edit than wireframes and meshes. 

You create basic solid shapes, such as a box, sphere, and wedge among others with the member methods and properties of the Solid3d object. You can also extrude region objects along a path or revolving a 2D object about an axis. 

Like meshes, solids are displayed as wireframes until you hide, shade, or render them. Additionally, you can analyze solids for their mass properties (volume, moments of inertia, center of gravity, and so forth). Use the following MassProperties property you can query the Solid3dMassProperties object associated with the Solid3d object. The Solid3dMassProperties object contains the following properties in which allow you to analyze the solid: MomentOfInertia, PrincipalAxes, PrincipalMoments, ProductOfInertia, RadiiOfGyration, and Volume.

The display of a solid is affected by the current visual style and 3D modeling related system variables. Some of the system variables that affect the display of a solid are ISOLINES and FACETRES. ISOLINES controls the number of tessellation lines used to visualize curved portions of the wireframe, while FACETRES adjusts the smoothness of shaded and hidden-line objects. 

## Create a wedge solid

The following example creates a wedge-shaped solid. The viewing direction of the active viewport is updated to display the three-dimensional nature of the wedge. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateWedge")]
    public static void CreateWedge()
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
    
            // Create a 3D solid wedge
            using (Solid3d acSol3D = new Solid3d())
            {
                acSol3D.CreateWedge(10, 15, 20);
    
                // Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(new Point3d(5, 5, 0) -
                                                            Point3d.Origin));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D);
                acTrans.AddNewlyCreatedDBObject(acSol3D, true);
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
     
    <CommandMethod("CreateWedge")> _
    Public Sub CreateWedge()
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
    
            '' Create a 3D solid wedge
            Using acSol3D As Solid3d = New Solid3d()
                acSol3D.CreateWedge(10, 15, 20)
    
                '' Position the center of the 3D solid at (5,5,0) 
                acSol3D.TransformBy(Matrix3d.Displacement(New Point3d(5, 5, 0) - _
                                                          Point3d.Origin))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSol3D)
                acTrans.AddNewlyCreatedDBObject(acSol3D, True)
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
    
    
    Sub CreateWedge()
        Dim wedgeObj As Acad3DSolid
        Dim center(0 To 2) As Double
        Dim length As Double
        Dim width As Double
        Dim height As Double
     
        ' Define the wedge
        center(0) = 5#: center(1) = 5#: center(2) = 0
        length = 10#: width = 15#: height = 20#
     
        ' Create the wedge in model space
        Set wedgeObj = ThisDrawing.ModelSpace. _
                           AddWedge(center, length, width, height)
     
        ' Change the viewing direction of the viewport
        Dim NewDirection(0 To 2) As Double
        NewDirection(0) = -1
        NewDirection(1) = -1
        NewDirection(2) = 1
        ThisDrawing.ActiveViewport.direction = NewDirection
        ThisDrawing.ActiveViewport = ThisDrawing.ActiveViewport
     
        ZoomAll
    End Sub
