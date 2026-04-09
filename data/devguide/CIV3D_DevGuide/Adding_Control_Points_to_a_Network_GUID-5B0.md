<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Adding Control Points to a Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5B07AE99-A314-453D-8B49-D7983E278555.htm -->

# Adding Control Points to a Network

Control points are the “known” or “fixed” locations that other survey points are based from. The collection of control points in a network is held in the AeccSurveyNetwork.ControlPoints property. New control points can be added to the network through the collection’s Create method. Create adds a new point with the specified features to the AeccSurveyControlPoints collection and returns a reference to the newly created AeccSurveyControlPoint object. 
    
    
    ' Get collection of all control points.
    Dim oControlPoints As AeccSurveyControlPoints
    Set oControlPoints = oSurveyNetwork.ControlPoints
     
    ' Create a control point with an id number of 3001 at 
    ' the location 5000.0m, 5000.0m, elevation 100.0m.
    Dim oControlPoint As AeccSurveyControlPoint
    Set oControlPoint = oControlPoints.Create( _
      3001, _
      "ControlPoint_01", _
      "Description of control point", _
      5000#, _
      5000#, _
      100#)
