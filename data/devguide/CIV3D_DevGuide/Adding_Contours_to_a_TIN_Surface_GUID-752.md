<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding Contours to a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-75295A16-B6C0-4C11-8A35-7824DD28489B.htm -->

# Adding Contours to a TIN Surface

A contour is an open or closed entity that describes the altitude of the surface along the entity. Contours must have a constant altitude. The z value of the first point of the entity is used as the altitude of entire entity, no matter what is specified in the following points. Contours also have settings that can adjust the number of points added to the surface - when you create a contour, you specify a weeding distance, a weeding angle, and a distance parameter. Points in the contour are removed if the distance between the points before and after is less than the weeding distance and if the angle between the lines before and after is less than the weeding angle. Each line segment is split into equal sections with a length no greater than the supplemental distance parameter. Any curves in the entity are also tessellated according to the mid-ordinate distance, just like breaklines. The supplemental distance value has precedence over the weeding values, so it is possible that the final contour will have line segments smaller than the weeding parameters specify. 

For more information about weeding and countours, see [About Weeding and Supplementing Factors for Contours](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-523368FB-BF6D-4E7C-8E38-7BA9A2B7E38A>). 

A TIN surface has a collection of contours in the AeccTinSurface.Contours property. The following sample demonstrates adding a contour to a surface: 
    
    
    Dim dPoints(0 To 8) As Double ' 3 points
    Dim o3DPoly As AcadPolyline
     
    dPoints(0) = 2500: dPoints(1) = 1500: dPoints(2) = 100
    dPoints(3) = 2600: dPoints(4) = 1600: dPoints(5) = 100
    ' It does not matter that we specify a Z value of 50. It 
    ' is still located at an altitude of 100, just like 
    ' the first point.
    dPoints(6) = 2400: dPoints(7) = 1600: dPoints(8) = 50
    Set o3DPoly = oAeccDocument.Database.ModelSpace _
      .AddPolyline(dPoints)
    o3DPoly.Closed = False
    Dim oEntities(0) As AcadEntity
    Set oEntities(0) = o3DPoly
     
    Dim dWeedDist as Double
    Dim dWeedAngle as Double
    Dim dDist as Double
    Dim dMidOrdDist as Double
    dWeedDist = 55.5
    dWeedAngle = 0.0698 ' 0.0698 radians = 4 degrees
    dDist = 85.5
    dMidOrdDist = 1#
    Dim oNewContour As AeccSurfaceContour
    Set oNewContour = oTinSurf.Contours.Add(oEntities, _
      "Sample Contour", dWeedDist, dWeedAngle, dDist, dMidOrdDist)
