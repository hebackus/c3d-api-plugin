<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Profiles in COM > Profiles > Creating a Profile Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A3BD9318-7454-4B0F-A609-7BBF77084951.htm -->

# Creating a Profile Style

The profile style, an object of type AeccProfileStyle, defines the visual display of profiles. The collection of all such styles in a document are stored in the AeccDocument.LandProfileStyles property. The style contains objects of type AeccDisplayStyle which govern the display of arrows showing alignment direction and of the lines, line extensions, curves, parabolic curve extensions, symmetrical parabolas and asymmetrical parabolas that make up a profile. The properties of a new profile style are defined by the document’s ambient settings.
    
    
    Dim oProfileStyle As AeccProfileStyle
    Set oProfileStyle = oDocument.LandProfileStyles
      .Add("Profile Style 01")
     
    ' For all profiles that use this style, line elements 
    ' will be yellow, curve elements will be shades of green,
    ' and extensions will be dark grey. No arrows will be shown.
    With oProfileStyle
       .ArrowDisplayStyleProfile.Visible = False
       .LineDisplayStyleProfile.Color = 50 ' yellow
       .LineDisplayStyleProfile.Visible = True
       .LineExtensionDisplayStyleProfile.Color = 251 ' grey
       .LineExtensionDisplayStyleProfile.Visible = True
       .CurveDisplayStyleProfile.Color = 80 ' green
       .CurveDisplayStyleProfile.Visible = True
       .ParabolicCurveExtensionDisplayStyleProfile.Color = 251 ' grey
       .ParabolicCurveExtensionDisplayStyleProfile.Visible = True
       .SymmetricalParabolaDisplayStyleProfile.Color = 81 ' green
       .SymmetricalParabolaDisplayStyleProfile.Visible = True
       .AsymmetricalParabolaDisplayStyleProfile.Color = 83 ' green
       .AsymmetricalParabolaDisplayStyleProfile.Visible = True
    End With
    ' Properties for 3d display should also be set.
