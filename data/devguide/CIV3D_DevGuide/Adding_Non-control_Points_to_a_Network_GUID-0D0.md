<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Adding Non-control Points to a Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0D05084F-CE37-41E9-85E8-414C6181CC62.htm -->

# Adding Non-control Points to a Network

A survey network also contains a collection of non-control points, which represent points within a survey network whose location is determined by observation, but are not connected to other survey observations and remain unaffected by a network analysis. These non-control points are represented by objects of type AeccNonControlPoint, and are defined by an easting, northing, and an optional elevation. The collection of all non-control points in a survey network are held in the AeccSurveyNetwork.NonControlPoints property.
    
    
    ' Create a non-control point with an id number of 3006 at 
    ' the location 4950.0, 5000.0, elevation 100.0.
    Dim oNonControlPt As AeccSurveyNonControlPoint
    Set oNonControlPt = oSurveyNetwork.NonControlPoints.Create( _
      3006, 
      "NonControlPoint_01",
      "Description of non-control point",
      4950#,
      5000#, 
      100#)
    

A non-control point may be promoted to a control point if you reference the point as a control point when creating a traverse, or reference the point as a setup to make observations to other points that may affect locations during an analysis.
