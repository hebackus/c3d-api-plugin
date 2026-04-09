<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Adding Setups to a Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CB48F0B9-073F-4227-835E-BF6B099B0D74.htm -->

# Adding Setups to a Network

A setup represents a survey instrument session made in the field. The instrument is set up on a control point or a previously observed point, and a reference direction (backsight) is made to another point. Locations on the Earth’s surface are then determined with surveying methods relative to the setup and the direction of the backsight. These locations are called “observations”, and are represented by an AeccSurveyObservation object. Each setup object contains a collection of observation objects. An observation object is composed of any or all of the following measurements: angle, distance, vertical, latitude, longitude, northing, easting, or elevation. The observation object also has a series of properties describing the nature of the observation equipment.

The collection of setups in a network is held in the AeccNetwork.Setups property. New setups can be added to the network through the collection’s Create method. Create adds a new setup at the specified location to the AeccSurveySetups collection and returns a reference to the newly created AeccSurveySetup object.

This sample creates a setup at the location of point 3001 using the location of point 3004 as the backsight. It then creates an observation to another location, which is given the identification “3002”.
    
    
    Dim oSetups As AeccSurveySetups
    Dim oSetup1 As AeccSurveySetup
     
    Set oSetups = oSurveyNetwork.Setups
    ' Create a setup at 3001 with a backsight at 3004 (the 
    ' backsight direction should be calculated automatically).
    Set oSetup1 = oSetups.Create(3001, 3004)
    Debug.Print "Direction:"; oSetup1.BacksightDirection
    Debug.Print "Orientation:"; oSetup1.BacksightOrientation
    ' Now any observation angle is based on the line 
    ' from 3001 to 3004.
     
    Dim oObservations As AeccSurveyObservations
    Set oObservations = oSetup1.Observations
    Dim oObservation1 As AeccSurveyObservation
    ' On setup "Station:3001, Backsight:3004" create an observation 
    ' of point 3002.
    '    Angle = 90 degrees (1.57079633 radians)
    '    Angle Type = Angle
    '    Distance = 100#
    '    Distance Type = Slope
    '    Vertical = 90 degrees (1.57079633 radians)
    '    Vertical Type = Vertical Angle
    '    Target Height = 0#
    '    Target Type = Prism
    Set oObservation1 = oObservations.Create( _
      3002, _
      aeccSurveyAngleTypeAngle, _
      1.57079633, _
      aeccSurveyDistanceTypeSlope, _
      100#, _
      aeccSurveyVerticalTypeVerticalAngle, _
      1.57079633, _
      aeccSurveyTargetTypePrism, _
      0#, _
      "From setup <Station:3001, Backsight:3004> to Point 3002")
     
    ' From this survey equipment data, the location of point
    ' 3002 can be determined:
    Debug.Print "Point 3002 at:"; oObservation1.Easting;
    Debug.Print ", "; oObservation1.Northing
