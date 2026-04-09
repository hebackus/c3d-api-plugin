<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Creating Paths for Traverse Analysis -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-03A316B7-1ADA-452E-AD35-E964B0AF30DB.htm -->

# Creating Paths for Traverse Analysis

A traverse is a path through survey points. A traverse starts at a control point, continues through other survey points, and either returns to the original control point (a “closed” loop) or ends at another control point (an “open” loop). These paths are used for traverse analysis, which are methods for determining the amount of error in the locations and directions of survey points. The API provides methods for creating and examining traverse paths, but it does not provide methods for performing a traverse analysis.

The collection of all traverses in a network are stored in the AeccSurveyNetwork.Traverses property. A single traverse is represented by an object of type AeccSurveyTraverse. New traverses are created using the collection’s Create method. This method requires the identification number of the starting control point, a backsight for that point, the final control point reached, and an array of the identification numbers of all intermediate points.

This sample creates a traverse starting at control point 3001, continuing though points 3002, 3003, and 3004, and finishing back at the starting control point 3001. The user can then perform a traverse analysis based on this closed loop.
    
    
    Dim oTraverse As AeccSurveyTraverse
    Dim lStations(0 To 2) As Long
    lStations(0) = 3002: lStations(1) = 3003; lStations(2) = 3004
    Set oTraverse = oSurveyNetwork.Traverses.Create( _
      "Traverse_01", _
      3001, _
      3004, _
      3001, _
      lStations)
