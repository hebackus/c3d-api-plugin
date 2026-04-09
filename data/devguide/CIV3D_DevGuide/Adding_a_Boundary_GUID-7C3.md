<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with Surfaces > Adding a Boundary -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7C32E309-9B54-42A0-A4DC-C6FD592071F2.htm -->

# Adding a Boundary

A boundary is a closed polygon that affects the visibility of the triangles inside it. 

All boundaries applied to a surface are stored in the Surface.BoundariesDefinition collection. The boundary itself is defined by an AutoCAD entity such as a closed polyline or polygon. The height of the entity plays no part in how surface triangles are clipped, so you can use 2D or 3D entities. This entity can also contain curves, but the boundary always consists of lines. How these lines are tessellated is defined by the mid-ordinate distance, which is the maximum distance between a curve and the lines that are generated to approximate it. 

You can add boundaries to a surface with its BoundariesDefinition.AddBoundaries() method. There are three overloads of this method that take one of these to define the new boundaries: 

  1. an ObjectIdCollection containing an existing polyline, polygon, or parcel 
  2. a Point2dCollection
  3. a Point3dCollection

This method also specifies the boundary type (data clip, outer, hide, or show), whether non-destructive breaklines should be used, and the mid-ordinate distance value, which determines how lines are tessellated from curves. 

In this example, the user is prompted to select a TIN surface and a polyline, and the polyline is added to the surface’s boundaries collection. Note that the surface must be re-built after the boundary is added. The re-build icon in the Civil 3D GUI is not displayed when a surface’s boundaries are modified using the .NET API. 
    
    
    [CommandMethod("AddSurfaceBoundary")]
    public void AddSurfaceBoundary()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Prompt the user to select a surface and a polyline
            ObjectId surfaceId = promptForEntity("Select the surface to add a boundary to", typeof(TinSurface));
            ObjectId polyId = promptForEntity("Select the object to use as a boundary", typeof(Polyline));
    
            // The boundary or boundaries must be added to an ObjectIdCollection for the AddBoundaries method:
            ObjectId[] boundaries = { polyId };
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
    
            try
            {
                oSurface.BoundariesDefinition.AddBoundaries(new ObjectIdCollection(boundaries), 100, Autodesk.Civil.SurfaceBoundaryType.Outer, true);
                oSurface.Rebuild();
            }
    
            catch (System.Exception e)
            {
                editor.WriteMessage("Failed to add the boundary: {0}", e.Message);
            }
    
            // commit the transaction
            ts.Commit();
        }
    }
