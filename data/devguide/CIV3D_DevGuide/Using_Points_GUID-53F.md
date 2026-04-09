<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Points > Using Points -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-53F2A717-1752-4F56-B026-CA5499B26F2C.htm -->

# Using Points

Each individual point is represented by an object of type AeccPoint. The point object contains the identification number, description, and location for the point. The identification number, held in the Point.Number property, is unique and is automatically assigned when the point is first created. It cannot be changed. The read-only Point.FullDescription property is only meaningful when the point is read from a file that contains description information.

You can access the local position through either the AeccPoint.Easting and AeccPoint.Northing properties or by using the AeccPoint.Location property, a three-element array containing the easting, northing, and elevation. The point’s location can also be specified by using the AeccPoint.Grideasting and AeccPoint.GridNorthing properties or the AeccPoint.Latitude and AeccPoint.Longitude properties, depending on the coordinate settings of the drawing. 

This sample adds a new point to the document’s collection of points and sets some of its properties.
    
    
    Dim oPoints As AeccPoints
    Set oPoints = g_oAeccDocument.Points
    Dim oPoint1 As AeccPoint
    Dim dLocation(0 To 2) As Double
    dLocation(0) = 4958
    dLocation(1) = 4078
    Set oPoint1 = oPoints.Add(dLocation)
    oPoint1.Name = "point1"
    oPoint1.RawDescription = "Point Description"
