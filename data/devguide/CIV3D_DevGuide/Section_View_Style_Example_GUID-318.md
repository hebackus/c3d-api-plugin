<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Section Views > Setting Section View Styles > Section View Style Example -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-31887501-4D50-4763-B710-993AA6F6090A.htm -->

# Section View Style Example

This example takes an existing section view style and modifies its top axis and title.
    
    
    ' We assume a section view style with the name
    ' "Section View style" already exists.
    Dim oSectionViewStyle As AeccSectionViewStyle
    Set oSectionViewStyle = oDocument.SectionViewStyles _
      .Item("Section View style")
     
    '''''''''''''''''''''''''''''''''''''
    ' Adjust the top axis.
    With oSectionViewStyle.TopAxis.MajorTickStyle
        .AnnotationDisplayStylePlan.color = 23 ' light brown
        .Height = 0.004 ' text height
        .AnnotationDisplayStylePlan.Visible = True ' show text
        .Interval = 15 ' Major ticks 15 ground units apart
        ' Each major tick is marked with distance from the 
        ' centerline in meters.
        .Text = "<[Section View Point Offset(Um|P1|RN|Sn|AP|OF)]>m"
        .DisplayStylePlan.Visible = True ' show ticks
    End With
    With oSectionViewStyle.TopAxis.TitleStyle
        .DisplayStylePlan.color = 23 ' light brown
        .Height = 0.008 ' text height
        .Text = "Meters"
        ' Position the title slightly higher.
        dOffset(0) = 0#
        dOffset(1) = 0.02
        .Offset = dOffset
        .DisplayStylePlan.Visible = True ' show title
    End With
     
    '''''''''''''''''''''''''''''''''''''
    ' Adjust the graph and graph title.
    With oSectionViewStyle.GraphStyle
        .VerticalExaggeration = 4.1
        ' The lowest grid with any part of the section
        ' line in it will have one empty grid between
        ' it and the bottom axis.
        .GridStyle.GridsBelowDatum = 1
        ' Increase the empty space above the section
        ' line to make room for any section line labels.
        .GridStyle.GridsAboveMaxElevation = 2
        
        ' Show major lines, but not minor lines.
        .GridStyle.MajorHorizontalDisplayStylePlan.Visible = True
        .GridStyle.MajorVerticalDisplayStylePlan.Visible = True
        .GridStyle.MinorHorizontalDisplayStylePlan.Visible = False
        .GridStyle.MinorVerticalDisplayStylePlan.Visible = False
     
        ' Move the title above the top axis.
        dOffset(0) = 0#
        dOffset(1) = 0.045
        .TitleStyle.Offset = dOffset
        ' Set the title to display the station number of each
        ' section.
        Dim sTmp as String
        sTmp = "EG at Station <[Section View Station(Uft|FS)]>"
        .TitleStyle.Text = sTmp
    End With
