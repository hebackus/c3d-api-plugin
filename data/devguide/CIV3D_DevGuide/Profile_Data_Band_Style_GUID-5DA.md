<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Profile Data Band Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5DAB3337-216D-42E7-B091-A0602D191016.htm -->

# Profile Data Band Style

Data bands for general information about profiles are defined by the AeccBandProfileDataStyle type. Information in this data band can be displayed at the major and minor grid marks of the base graph, at points where the alignment station equation changes, and at points where the vertical or horizontal geometry change.

Each label can use any of the following property fields: 

Valid property fields for use with AeccBandLabelStyle text components  
---  
<[Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Raw Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile1 Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[Profile2 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Profile1 Elevation Minus Profile2 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Profile2 Elevation Minus Profile1 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
  
This sample demonstrates the creation of a data band style displaying section elevation data at two different locations:
    
    
    Dim oBandProfileDataStyle As AeccBandProfileDataStyle
    Set oBandProfileDataStyle = oDocument.ProfileViewBandStyles _
      .ProfileDataBandStyles.Add("Profile Band")
     
     
    With oBandProfileDataStyle
        ' Add ticks and labels to each horizontal 
        ' geography location.
        .HGPLabelDisplayStylePlan.Visible = True
        .HGPTickDisplayStylePlan.Color = 10 ' red
        .HGPTickDisplayStylePlan.Visible = True
        .HGPLabelStyle.TextComponents.Item(0).Contents = _
          "<[Station Value(Uft|FS|P0|RN|AP|Sn|TP|B2|EN|W0|OF)]>"
        .HGPLabelStyle.TextComponents.Item(0).Color = 11 ' red
        .HGPLabelStyle.TextComponents.Item(0).Visibility = True
     
        ' Modify how the title is displayed.
        .TitleBoxDisplayStylePlan.Color = 10 ' red
        .TitleBoxDisplayStylePlan.Linetype = "DOT"
        .TitleBoxDisplayStylePlan.Visible = True
        .TitleBoxTextDisplayStylePlan.Color = 80 ' green
        .TitleBoxTextDisplayStylePlan.Visible = True
        .TitleStyle.Text = "Profile Info"
        .TitleStyle.TextHeight = 1.0
        .TitleStyle.TextBoxWidth = 2.0
     
        ' Hide the rest of the information locations.
        .VGPLabelStyle.TextComponents.Item(0).Visibility = False
        .MajorIncrementLabelStyle.TextComponents.Item(0). _
          Visibility = False
        .MajorStationLabelDisplayStylePlan.Visible = False
        .MajorTickDisplayStylePlan.Visible = False
        .MinorIncrementLabelStyle.TextComponents.Item(0). _
          Visibility = False
        .MinorStationLabelDisplayStylePlan.Visible = False
        .MinorTickDisplayStylePlan.Visible = False
        .VGPLabelDisplayStylePlan.Visible = False
        .VGPTickDisplayStylePlan.Visible = False
        .StationEquationLabelStyle.TextComponents.Item(0). _
          Visibility = False
        .StationEquationLabelDisplayStylePlan.Visible = True
        .StationEquationTickDisplayStylePlan.Visible = True
    End With
    

This style produces a data band that looks like this:
