<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Sample Lines > Creating Sample Line Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5D91EB54-7126-467C-8C1E-9B51A311AD88.htm -->

# Creating Sample Line Styles

In creating sample lines, you need to work with three different style objects that control how sample lines are displayed.

## Group Plot Styles

The AeccGroupPlotStyle style controls how groups of section view graphs are drawn. The style changes the row and column orientation and spacing between multiple graphs. The collection of all AeccGroupPlotStyle styles is contained in the AeccDocument.GroupPlotStyles property. 
    
    
    Dim oGroupPlotStyle As AeccGroupPlotStyle
    Set oGroupPlotStyle = oDocument.GroupPlotStyles _
      .Add("Example group plot style")
    

## Sample Line Styles

The AeccSampleLineStyle style controls how sample lines are drawn on a surface. The collection of all AeccSampleLineStyle styles is contained in the AeccDocument.SampleLineStyles property. 
    
    
    Dim oSampleLineStyle As AeccSampleLineStyle
    Set oSampleLineStyle = oDocument.SampleLineStyles _
      .Add("Example sample line style")
     
    ' This style just changes the display of the sample line.
    oSampleLineStyle.LineDisplayStyleSection.color = 140 ' slate
    

## Section Styles

The AeccSectionStyle style controls how surface cross sections are displayed in the section view graphs. The collection of all AeccSectionStyle styles is contained in the AeccDocument.SectionStyles property. 
    
    
    Dim oSectionStyle As AeccSectionStyle
    Set oSectionStyle = oDocument.SectionStyles _
      .Add("Example cross section style")
     
    ' This style just changes the display of cross section
    ' lines.
    oSectionStyle.SegmentDisplayStyleSection.color = 110 ' green/blue
