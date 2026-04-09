<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Profiles in COM > Profiles > Creating a Profile Using Entities -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-409176A7-99F7-462A-A2E0-30449957CAB6.htm -->

# Creating a Profile Using Entities

The AeccProfiles.Add method creates a new profile with no elevation information. The vertical shape of a profile can then be specified using entities. Entities are geometric elements - tangents or symmetric parabolas. The collection of all entities that make up a profile are contained in the AeccProfile.Entities collection. AeccProfile.Entities also contains all the methods for creating new entities.

This sample creates a new profile along the alignment “oAlignment” and then adds three entities to define the profile shape. Two straight entities are added at each end and a symmetric parabola is added in the center to join them and represent the sag of a valley.
    
    
    Dim oProfiles As AeccProfiles
    Set oProfiles = oAlignment.Profiles
    Dim oProfile As AeccProfile
     
    ' NOTE: The second parameter (aeccFinishedGround) indicates
    ' that the shape of the profile is not drawn from the existing
    ' surface. We will define the profile ourselves. 
    Set oProfile = oProfiles.Add _
      ("Profile03", _
      aeccFinishedGround, _
      oProfileStyle.Name)
     
    ' Now add the entities that define the profile.
    ' NOTE: Profile entity points are not x,y,z point, but
    ' station-elevation locations.
    Dim dLoc1(0 To 1) As Double
    Dim dLoc2(0 To 1) As Double
    Dim oProfileTangent1 As aeccProfileTangent
    dLoc1(0) = oAlignment.StartingStation: dLoc1(1) = -40#
    dLoc2(0) = 758.2: dLoc2(1) = -70#
    Set oProfileTangent1 = oProfile.Entities.AddFixedTangent _
      (dLoc1, dLoc2)
     
    Dim oProfileTangent2 As aeccProfileTangent
    dLoc1(0) = 1508.2: dLoc1(1) = -60#
    dLoc2(0) = oAlignment.EndingStation: dLoc2(1) = -4#
    Set oProfileTangent2 = oProfile.Entities.AddFixedTangent _
      (dLoc1, dLoc2)
     
    Dim dCrestLen As Double
    dCrestLen = 900.1
    Call oProfile.Entities.AddFreeSymmetricParabolaByLength _
      (oProfileTangent1.Id, _
      oProfileTangent2.Id, _
      aeccSag, _
      dCrestLen, _
      True)
