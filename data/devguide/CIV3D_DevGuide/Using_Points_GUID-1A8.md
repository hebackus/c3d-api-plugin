<!-- Developer's Guide > API Developer's Guide > Points > Using Points -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1A8EEBDB-2D04-472C-979E-CB3B6FD2A296.htm -->

# Using Points

Coordinated Geometry Points (COGO points) are more complex than AutoCAD point nodes, which have only coordinate data. A CogoPoint object, in addition to a location, also has properties such as a unique ID number, name, raw (field) description, and full (expanded) description. The point number is unique, and is automatically assigned when the point is created. You can change the point number either by setting the PointNumber property directly, or by using the Renumber() method. Setting the property directly will throw an exception if another point exists with the specified value, while the Renumber() method will use the settings for resolving point numbering conflicts to choose another point number. You can also set the PointNumber property for multiple points using the CogoPointCollection.SetPointNumber() method. 

The full description property is read-only once a point is created. 

The CogoPoint object’s Location property is read-only. However, you can read and change the local position using the Easting, Northing and Elevation properties. The point’s location can also be specified by using the Grideasting and GridNorthing properties or the Latitude and Longitude properties, depending on the coordinate and transformation settings of the drawing. 

A CogoPoint object is either a drawing point or a project point. Project points have the isProjectPoint property set to true, and have additional project information contained by the IsCheckedOut and ProjectVersion properties. Attempting to get or set these properties for points that have isProjectPoint == false raises an exception, so it is a good idea to check that property first. 

CogoPoint objects also have several read-only override properties that contain values that have been overridden by PointGroup settings. These include ElevationOverride, FullDescriptionOverride, LabelStyleIdOverride, RawDescriptionOverride, and StyleIdOverride. 

This sample adds a new point to the document’s collection of points and sets some of its properties. 
    
    
    [CommandMethod("C3DSAMPLES", "CreatePoint", CommandFlags.Modal)]
    public void CreatePoint()
    {
        using (Transaction tr = startTransaction())
        {
            // _civildoc is the active CivilDocument instance.
            Point3d location = new Point3d(4958, 4079, 200);
            CogoPointCollection cogoPoints = _civildoc.CogoPoints;
            ObjectId pointId = cogoPoints.Add(location);
            CogoPoint cogoPoint = pointId.GetObject(OpenMode.ForWrite) as CogoPoint;
            cogoPoint.PointName = "point1";
            cogoPoint.RawDescription = "Point description";
    
            tr.Commit();
        }
    }
