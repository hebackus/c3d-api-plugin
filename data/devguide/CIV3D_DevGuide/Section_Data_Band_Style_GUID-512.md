<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Section Data Band Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-512D4316-5F09-49E2-97C0-78EE26BBDD73.htm -->

# Section Data Band Style

Data bands for section views are described by an object of type AeccBandSectionDataStyle. Information in this data band can be displayed at major and minor tick marks, at the centerline, at each section grade break, and at each sample line vertex. The centerline is the location where the sample line crosses the alignment. If the sample line does not cross the alignment, the centerpoint is where the sample line would cross the alignment if the sample line were extended. Unless the AeccSampleLines.AddByPolyline method was used to create a multi-segment sample line, placing information at each sample line vertex simply places tick marks and labels at the section endpoints.

Each label style can use any of the following property fields: 

Valid property fields for use with AeccBandLabelStyle text components  
---  
<[Distance from Centerline(Uft|P2|RN|Sn|OF|AP)]>  
<[Distance from Centerline Side(CP)]>  
<[Offset from Centerline(Uft|P3|RN|AP|Sn|OF)]>  
<[Offset from Centerline Side(CP)]>  
<[Section1 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Section2 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Section1 Elevation Minus Section2 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Section2 Elevation Minus Section1 Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Section Segment Grade In(FP|P2|RN|AP|Sn|OF)]>  
<[Section Segment Grade Out(FP|P2|RN|AP|Sn|OF)]>  
<[Section Segment Grade Change(FP|P2|RN|AP|Sn|OF)]>  
  
This sample demonstrates the creation of a data band style displaying section elevation data at two different locations:
    
    
    Dim oBandSectionDataStyle As AeccBandSectionDataStyle
    Set oBandSectionDataStyle = oDocument.SectionViewBandStyles. _
      SectionDataBandStyles.Add("Segment Band")
     
     
    ' Display at every major grid line a tick mark and a label
    ' that shows the section elevation at that point.
    With oBandSectionDataStyle
        .MajorOffsetLabelDisplayStylePlan.Color = 255 ' white
        .MajorOffsetLabelDisplayStylePlan.Visible = True
        .MajorOffsetTickDisplayStylePlan.Color = 255 ' white
        .MajorOffsetTickDisplayStylePlan.Visible = True
    End With
    With oBandSectionDataStyle.MajorIncrementLabelStyle. _
      TextComponents.Item(0)
        .Contents = "<[Section1 Elevation(Um|P3|RN|AP|Sn|OF)]>m"
        .Color = 255 ' white
        .Visibility = True
        ' Shift the label to the high side of the band.
        .YOffset = 0.015
    End With
     
     
    ' Display a red tick mark and a red label showing section 
    ' elevation at each vertex endpoint in the sample line.
    ' Make the tick mark large, and only at the top of the 
    ' band.
    With oBandSectionDataStyle
        .SampleLineVertexLabelDisplayStylePlan.Color = 20 ' red
        .SampleLineVertexLabelDisplayStylePlan.Visible = True
        .SampleLineVertexTickDisplayStylePlan.Color = 20 ' red
        .SampleLineVertexTickDisplayStylePlan.Visible = True
    End With
    With oBandSectionDataStyle.SampleLineVerticesLabelStyle. _
      TextComponents.Item(0)
        .Contents = "<[Section1 Elevation(Um|P3|RN|AP|Sn|OF)]>m"
        .Color = 20 ' red
        .Visibility = True
        .YOffset = 0.08
    End With
    With oBandSectionDataStyle.SampleLineVerticesLabelStyle. _
      TickStyle
        .IncrementSmallTicksAtTop = True
        .IncrementSmallTicksAtMiddle = False
        .IncrementSmallTicksAtBottom = False
        .SmallTicksAtTopSize = 0.015
    End With
     
     
    ' Hide all other data locations in the data band.
    With oBandSectionDataStyle
        .CenterLineLabelDisplayStylePlan.Visible = False
        .CenterLineTickDisplayStylePlan.Visible = False
        .GradeBreakLabelDisplayStylePlan.Visible = False
        .GradeBreakTickDisplayStylePlan.Visible = False
        .MinorOffsetLabelDisplayStylePlan.Visible = False
        .MinorOffsetTickDisplayStylePlan = False
    End With
    

This style produces a data band that looks like this:
