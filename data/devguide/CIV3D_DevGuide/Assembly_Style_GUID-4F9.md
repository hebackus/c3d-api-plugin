<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Styles > Assembly Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4F9C98F1-7085-4A13-B682-00D2DD9CAFFA.htm -->

# Assembly Style

The collection of all assembly style objects are found in the AeccRoadwayDocument.AssemblyStyles property. The assembly style object contains properties for adjusting the marker types for the assembly attachment points, each of the standard AeccMarkerType property. While you can create new styles and edit existing styles, you cannot assign a style to an existing assembly using the Autodesk Civil 3D API.
    
    
    ' Create a new assembly style and change it so that the
    ' place where the assembly attaches to the main baseline
    ' is marked with a red X.
    Dim oAssemblyStyle As AeccAssemblyStyle
    Set oAssemblyStyle = oRoadwayDocument.AssemblyStyles.Add("Style1")
    With oAssemblyStyle.MarkerStyleAtMainBaseline
        .CustomMarkerStyle = aeccCustomMarkerX
        .MarkerDisplayStylePlan.Color = 10 ' red
        .MarkerDisplayStylePlan.Visible = True
    End With
