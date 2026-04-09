<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Vertical Geometry Data Band Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C3BEB467-F192-4FF7-B1B4-31C3DA3FA1A6.htm -->

# Vertical Geometry Data Band Style

The AeccBandProfileDataStyle type is used to display features of the vertical geometry of alignments in profile views. The style of graphical markers displayed at each curve and tangent segment can be modified, as well as the labels placed at crest, sag, uphill, and downhill segments of the profile.

Downhill and uphill labels can use any of the following property fields: 

Valid property fields for use with AeccBandLabelStyle text components  
---  
<[Tangent Horizontal Length(Uft|P2|RN|Sn|OF|AP)]>  
<[Tangent Slope Length(Uft|P2|RN|AP|Sn|OF)]>  
<[Tangent Grade(FP|P2|RN|AP|Sn|OF)]>  
<[Tangent Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Tangent Start Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[Tangent End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Tangent End Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[Tangent Elevation Change(Uft|P2|RN|AP|Sn|OF)]>  
<[PVI Before Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[PVI Before Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[PVI After Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[PVI After Elevation(Uft|P2|RN|AP|Sn|OF)]>  
  
This sample demonstrates the creation of a data band style displaying the direction of slope for all segments of a profile with a title:
    
    
    Dim oBandVerticalGeometryStyle As AeccBandVerticalGeometryStyle
    Set oBandVerticalGeometryStyle = oDocument.ProfileViewBandStyles _
      .VerticalGeometryBandStyles.Add("Vertical Band")
     
     
     With oBandVerticalGeometryStyle
        ' Add graphical marks that show the uphill or downhill
        ' directions and the lengths of the vertical segments
        ' of the profile.  On uphill sections the label of the
        ' length of the segment will be in white, on downhill
        ' it will be pale yellow. The graphical element that
        ' shows direction will be pink.
        .DownhillTangentLabelStyle.TextComponents.Item(0).
          Contents = "<[Tangent Horizontal Length(Uft|P2)]>"
        .DownhillTangentLabelStyle.TextComponents.Item(0). _
          Color = 51 ' pale yellow
        .DownhillTangentLabelStyle.TextComponents.Item(0). _
          Visibility = True
        .UphillTangentLabelStyle.TextComponents.Item(0).
          Contents = "<[Tangent Horizontal Length(Uft|P2)]>"
        .UphillTangentLabelStyle.TextComponents.Item(0). _
          Color = 255  ' white
        .UphillTangentLabelStyle.TextComponents.Item(0). _
          Visibility = True
        .TangentGeometryDisplayStylePlan.Color = 220 ' pink
        .TangentGeometryDisplayStylePlan.Visible = True
        .TangentLabelDisplayStylePlan.Visible = True
        .TangentGeometryDisplayStylePlan.Visible = True
     
        ' Modify how the title is displayed.
        .TitleBoxDisplayStylePlan.Color = 10 ' red
        .TitleBoxDisplayStylePlan.Linetype = "DOT"
        .TitleBoxDisplayStylePlan.Visible = True
        .TitleBoxTextDisplayStylePlan.Color = 80 ' green
        .TitleBoxTextDisplayStylePlan.Visible = True
        .TitleStyle.Text = "Profile Geometry"
        .TitleStyle.TextHeight = 0.0125
        .TitleStyle.TextBoxWidth = 0.21
     
        ' Hide the rest of the information locations and
        ' graphical displays.
        .CurveGeometryDisplayStylePlan.Visible = False
        .CurveLabelDisplayStylePlan.Visible = False
        .TickDisplayStylePlan.Visible = False
    End With
    

This style produces a data band that looks like this:
