<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Adding Directions to a Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-20927900-AAB9-4281-A3FC-30A129ECF51C.htm -->

# Adding Directions to a Network

A direction is a “known” or “fixed” direction (either azimuth or bearing) from a control point to another point reference. The point reference may be observed at a later time in the survey, or it may never actually be occupied by a setup. This can happen if the reference point is a mountain top or tower or some other location where survey equipment cannot physically be placed but the direction from the control point to that location is known. An entire survey network can be defined from a single control point and a single direction.

The collection of directions in a network is held in the AeccNetwork.Directions property. New directions can be added to the network through the collection’s Create method. Create adds a new direction between two points at the specified angle to the AeccSurveyDirections collection and returns a reference to the newly created AeccSurveyDirection object.
    
    
    ' Get collection of all directions.
    Dim oDirections As AeccSurveyDirections
    Set oDirections = oSurveyNetwork.Directions
     
    ' Create a direction from point 3001 to the (not yet
    ' existing) point 3004 at an angle of 45.0 degrees azimuth.
    Dim oDirection As AeccSurveyDirection
    ' 0.785398163 = 40 degrees in radians
    Set oDirection = oDirections.Create( _
      3001, _
      3004, _
      0.785398163, _
      aeccSurveyDirectionTypeAzimuth)
