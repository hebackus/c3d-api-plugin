<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Analysis > Calculating Bounded Volumes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DA353D59-E5F2-4CE7-BFE9-1117EE9A8942.htm -->

# Calculating Bounded Volumes

The .NET API exposes the Civil 3D Bounded Volumes Utility as the GetBoundedVolumes() method for the Surface class, which means that bounded volumes can be calculated for both TIN and Grid surfaces. This method takes a Point3dCollection containing points that define the vertices of a polygon area, and an optional elevation datum. If you do not supply an elevation datum, the method uses 0.0. The first and last point in the vertices collection must be the same; that is, the polygon must be closed. The method returns a SurfaceVolumeInfo object that includes values for net volume, cut volume, and fill volume. 

In this example, a sample TIN surface is created, a polygon inside the surface is defined, and both versions of the GetBoundedVolumes() method is called on the surface. 
    
    
    // Create a sample surface
    ObjectId surfaceId = TinSurface.Create(_acaddoc.Database, "Example Surface");
    TinSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
    
    // Generates 100 random points between 0,100:
    Point3dGenerator p3dgen = new Point3dGenerator();
    Point3dCollection locations = p3dgen.AsPoint3dCollection();
    surface.AddVertices(locations);
     
    // Create a region that is a polygon inside the surface.
    // The first and last point must be the same to create a closed polygon.
    //
    Point3dCollection polygon = new Point3dCollection();
    polygon.Add(new Point3d(20, 20, 20));
    polygon.Add(new Point3d(20, 80, 15));
    polygon.Add(new Point3d(80, 40, 25));
    polygon.Add(new Point3d(20, 20, 20));
    double elevation = 30.5;
    
    SurfaceVolumeInfo surfaceVolumeInfo = surface.GetBoundedVolumes(polygon, elevation);
    write(String.Format("Surface volume info:\n  Cut volume: {0}\n Fill volume: {1}\n Net volume: {2}\n",
        surfaceVolumeInfo.Cut, surfaceVolumeInfo.Fill, surfaceVolumeInfo.Net));
    
    // If you do not specify an elevation, 0.0 is used:
    //
    surfaceVolumeInfo = surface.GetBoundedVolumes(polygon);
    write(String.Format("Surface volume info:\n  Cut volume: {0}\n Fill volume: {1}\n Net volume: {2}\n",
        surfaceVolumeInfo.Cut, surfaceVolumeInfo.Fill, surfaceVolumeInfo.Net));
