<!-- Developer's Guide > API Developer's Guide > Points > Using the Points Collection -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D010B84F-F579-4960-9892-A7FCF49FE450.htm -->

# Using the Points Collection

All points in a document are held in a CogoPointCollection object accessed through the CivilDocument.CogoPoints property. In addition to the common collection properties and methods, this collection also exposes methods for working with large numbers of points at once. For example, points can be added to the collection either individually, or from a Point3dCollection. 

The following sample adds a collection of randomly generated points to the document’s point collection, and then accesses each point in the collection directly to calculate the average elevation: 
    
    
    [CommandMethod("C3DSAMPLES", "AverageCogoElevation", CommandFlags.Modal)]
    public void AverageCogoElevation()
    {
        using (Transaction tr = startTransaction())
        {
    
            // _civildoc is the active CivilDocument instance.
            CogoPointCollection cogoPoints = _civildoc.CogoPoints;
            Point3d[] points = { new Point3d(4927, 3887, 150), new Point3d(5101, 3660, 250), new Point3d(5144, 3743, 350) };
            Point3dCollection locations = new Point3dCollection(points);
    
            cogoPoints.Add(locations);
    
            // Compute the average elevation of all the points in a document.
            double avgElevation = 0;
            foreach (ObjectId pointId in cogoPoints)
            {
                CogoPoint cogoPoint = pointId.GetObject(OpenMode.ForRead) as CogoPoint;
                avgElevation += cogoPoint.Elevation;
            }
    
            avgElevation /= cogoPoints.Count;
            _editor.WriteMessage("Average elevation: {0} \nNumber of points: {1}", avgElevation, cogoPoints.Count);
            tr.Commit();
        }
    }
