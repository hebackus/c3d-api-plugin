<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Extracting Contours -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FAB219E9-235B-4E41-8E2F-6ED10DE07577.htm -->

# Extracting Contours

Contours can be extracted as AutoCAD drawing objects from surfaces (both TIN and Grid) using versions of ExtractContours(), ExtractContoursAt(), ExtractMajorContours(), and ExtractMinorContours(). These methods are defined by the ITerrainSurface interface, and implemented by all Surface classes. 

The four methods are very similar, but accomplish different things: 

  * ExtracContours() \- this method extracts contours at a specified elevation interval, starting at the surface's lowest elevation. 
  * ExtractContoursAt() \- this method extracts all contours at a single specified elevation. 
  * ExtractMajorContours() \- this method extracts only major contours from a Surface. 
  * ExtractMinorContours() \- this method extracts only minor contours from a Surface. 

The ExtractContours() method has four versions, the simplest taking an interval parameter, and another taking an elevation range and interval. There are also versions of these two methods that take additional smoothing parameters to smooth the extracted polylines. The extracted contours are lightweight AutoCAD Polyline objects, and the method returns an ObjectIdCollection containing the IDs of all extracted objects. The objects are independent of the surface and can be manipulated without affecting the underlying surface. 

This example creates a random surface, and then extracts contours in a couple of ways. 
    
    
    // Setup: creates a new, random surface
    // 
    TinSurface surface = CreateRandomSurface("Example Surface");
    
    // Extract contours and print information about them:
    ObjectIdCollection contours;
    double contourInterval = 50.0;
    contours = surface.ExtractContours(contourInterval);
    write("# of extracted contours: " + contours.Count + "\n");
    int totalVertices = 0;
    for (int i = 0; i < contours.Count; i++)
    {
        ObjectId contourId = contours[i];
    
        // Contours are lightweight Polyline objects:
        Polyline contour = contourId.GetObject(OpenMode.ForRead) as Polyline;
        write(String.Format("Contour #{0} length:{1}, # of vertices:{2}\n",
            i, contour.Length, contour.NumberOfVertices));
        totalVertices += contour.NumberOfVertices;
    }
    
    // Extract contours with smoothing:
    contours = surface.ExtractContours(contourInterval, ContourSmoothingType.AddVertices, 10);
    int totalVerticesSmoothed = 0;
    foreach (ObjectId contourId in contours)
    {
        Polyline contour = contourId.GetObject(OpenMode.ForRead) as Polyline;
        totalVerticesSmoothed += contour.NumberOfVertices;
    }
    
    // Compare smoothing by adding vertices:
    write(String.Format("Effects of smoothing:\n  total vertices no smoothing: {0}\n  total vertices with smoothing: {1}\n",
        totalVertices, totalVerticesSmoothed));
    
    // Extract contours in a range:
    double startRange = 130.0;
    double endRange = 190.0;
    contours = surface.ExtractContours(contourInterval, startRange, endRange);
    
    write("# of extracted contours in range: " + contours.Count + "\n");
    
    // You can also extract contours in a range with smoothing:
    // contours = surface.ExtractContours(contourInterval, startRange, endRange, 
    //    ContourSmoothingType.SplineCurve, 10);
