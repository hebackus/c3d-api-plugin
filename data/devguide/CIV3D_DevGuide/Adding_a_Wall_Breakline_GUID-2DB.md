<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding a Breakline to a TIN Surface > Adding a Wall Breakline -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2DB9FC3A-4D9B-483E-8FB6-431CEEE37B2A.htm -->

# Adding a Wall Breakline

A wall breakline is used when the height of the surface on one side of the breakline is different than the other side. This method creates two breaklines, one for the top of the wall and one for the bottom. However, you cannot have a perfectly vertical wall in a TIN surface. The first breakline is placed along the path specified by the BreaklineEntities parameter, and the second breakline is very slightly offset to one side and raised or lowered by a relative elevation. Among the parameters of the wall breakline creation method are an array of wall elevations and an array describing to which side the height-adjusted breakline is placed. The wall at each entity endpoint is offset to the right if the value is set to True and to the left of the value is set to False where “right” and “left” refer to directions as you walk along the breakline from the start point to the end. 
    
    
    ' This is an array of arrays of elevations, one array of
    ' elevations per entity.
    Dim vElevations(0) As Variant
    ' These are the elevations of the wall at each endpoint in
    ' the polyline entity.
    Dim dElevations(3) As Double
    ' This is an array of ooleans, one for each entity.
    Dim bOffsets(0) As Boolean
     
    dElevations(0) = 30.5: dElevations(1) = 93.3
    dElevations(2) = 93.3: dElevations(3) = 46.2
    vElevations(0) = dElevations
    ' Raise the surface at the right side of the breakline.
    bOffsets(0) = True: bOffsets(1) = True
    bOffsets(2) = True: bOffsets(3) = True
     
    Set oBreakline = oTinSurf.Breaklines.AddWallBreakline _
      (oEntityArray, _
      "Sample Wall Break", _
      1#, _
      vElevations, _
      bOffsets)
