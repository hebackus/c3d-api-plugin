<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Adding Contours to a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E1262924-0A6D-4BF1-B5C5-945CC3065A25.htm -->

# Adding Contours to a TIN Surface

A contour is an open or closed entity that describes the altitude of the surface along the entity. Contours must have a constant altitude. The z value of the first point of the entity is used as the altitude of entire entity, no matter what is specified in the following points. Contours also have settings that can adjust the number of points added to the surface - when you create a contour, you specify a weeding distance, a weeding angle, and a distance parameter. Points in the contour are removed if the distance between the points before and after is less than the weeding distance and if the angle between the lines before and after is less than the weeding angle. Each line segment is split into equal sections with a length no greater than the maximumDistance parameter. Any curves in the entity are also tessellated according to the mid-ordinate distance, just as with breaklines. The maximumDistance value has precedence over the weeding values, so it is possible that the final contour will have line segments smaller than the weeding parameters specify. 

Contours can be added from a Point2dCollection, Point3dCollection, or an ObjectIdCollection containing polylines. You can optionally specify options for minimizing flat areas in a surface by passing a SurfaceMinimizeFlatAreaOptions object as a parameter to SurfaceDefinitionContours.AddContours(). For more information about the ways you can minimize flat areas, see “Minimizing Flat Areas in a Surface” in the Civil 3D user’s Guide. 

The following sample demonstrates adding a contour to a surface from a polyline: 
    
    
    [CommandMethod("CreateContour")]
    public void CreateContour()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Prompt the user to select a TIN surface and a polyline, and create a contour from the polyline
            ObjectId surfaceId = promptForEntity("Select a TIN surface to add a contour to", typeof(TinSurface));
            ObjectId polyId = promptForEntity("Select a polyline to create a contour from", typeof(Polyline));
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;                
            ObjectId[] contours = {polyId};              
    
            oSurface.ContoursDefinition.AddContours(new ObjectIdCollection(contours), 1, 85.5, 55.5, 0);
    
            // commit the transaction
            ts.Commit();
        }
    }
