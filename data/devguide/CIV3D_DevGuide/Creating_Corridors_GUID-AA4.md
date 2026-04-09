<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Corridors > Creating Corridors -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AA420ECC-ED85-45D2-BCC9-78DCD591C40D.htm -->

# Creating Corridors

The corridors collection includes a AeccCorridors.Add method for creating new corridors. This method creates the corridor based on an existing alignment, profile, and assembly.

Note:

The station distance between assemblies cannot be set through the API, and needs to be set through the property page dialog box before the AeccCorridors.Add method is called.
    
    
    ' Assuming oAlignment, oProfile, and oAssembly represent
    ' valid AeccAlignment, AeccProfile, and AeccAssembly objects.
    Dim oCorridors As AeccCorridors
    Set oCorridors = oRoadwayDocument.Corridors
    Dim oCorridor As AeccCorridor
    Set oCorridor = oCorridors.Add( _
      "Corridor01", _
      oAlignment.Name, _
      oProfile.Name, _
      oAssembly.Name)
