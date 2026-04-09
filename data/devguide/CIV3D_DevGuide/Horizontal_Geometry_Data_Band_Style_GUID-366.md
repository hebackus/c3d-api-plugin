<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Horizontal Geometry Data Band Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-366BDB73-3905-4134-988E-337A66C9353C.htm -->

# Horizontal Geometry Data Band Style

The AeccBandHorizontalGeometryStyle type is used to display features of the horizontal geometry of alignments in profile views. Tangents and curves in the alignment are displayed as stylized line segments and curve segments, and a label can be displayed over each segment.

Each label style can use any of the following property fields: 

Valid property fields for use with AeccBandLabelStyle text components  
---  
<[Length(Uft|P2|RN|Sn|OF|AP)]>  
<[Tangent Direction(Udeg|FDMSdSp|MB|P6|RN|DSn|CU|AP|OF)]>  
<[Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Start Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Start Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[End Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[End Northing(Uft|P4|RN|AP|Sn|OF)]>  
  
This sample demonstrates the creation of a data band style displaying information about alignment geometry with a title:
    
    
    Dim oBandProfileDataStyle As AeccBandProfileDataStyle
    Set oBandProfileDataStyle = oDocument.ProfileViewBandStyles _
      .ProfileDataBandStyles.Add("Horizontal Band")
     
     
    With oBandHorizontalGeometryStyle
        ' Add displays and labels for alignment tangents.
        .TangentGeometryDisplayStylePlan.Visible = True
        .TangentGeometryDisplayStylePlan.Color = 160 ' blue
        .TangentLabelDisplayStylePlan.Visible = True
        .TangentLabelStyle.TextComponents.Item(0).Contents = _
          "Length = <[Length(Uft|P2|RN|Sn|OF|AP)]>"
        .TangentLabelStyle.TextComponents.Item(0).Color = 120
        .TangentLabelStyle.TextComponents.Item(0). _
          Visibility = True
     
        ' Add displays and labels for alignment curves.
        .CurveGeometryDisplayStylePlan.Visible = True
        .CurveGeometryDisplayStylePlan.Color = 160 ' blue
        .CurveLabelDisplayStylePlan.Visible = True
        .CurveLabelStyle.TextComponents.Item(0).Contents = _
          "Length = <[Length(Uft|P2|RN|Sn|OF|AP)]>"
        .CurveLabelStyle.TextComponents.Item(0).Color = 120
        .CurveLabelStyle.TextComponents.Item(0). _
          Visibility = True
     
        ' Add tick marks at each horizontal geometry point,
        ' the location where different segments of the
        ' alignment meet. 
        .TickDisplayStylePlan.Color = 10 ' red
        .TickDisplayStylePlan.Visible = True
     
        ' Modify how the title is displayed.
        .TitleBoxDisplayStylePlan.Color = 10 ' red
        .TitleBoxDisplayStylePlan.Linetype = "DOT"
        .TitleBoxDisplayStylePlan.Visible = True
        .TitleBoxTextDisplayStylePlan.Color = 80 ' green
        .TitleBoxTextDisplayStylePlan.Visible = True
        .TitleStyle.Text = "Alignment Geometry"
        .TitleStyle.TextHeight = 0.0125
        .TitleStyle.TextBoxWidth = 0.21 
        ' Hide the rest of the information locations and
        ' graphical displays.
        .SpiralGeometryDisplayStylePlan.Visible = False
        .SpiralLabelDisplayStylePlan.Visible = False
    End With
    

This style produces a data band that looks like this:
