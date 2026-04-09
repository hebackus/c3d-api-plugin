<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Sample Lines > Creating a Sample Line -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3B48FADD-FC6E-4E15-B67F-B226DECF8F74.htm -->

# Creating a Sample Line

Sample lines are line segments placed along an alignment, usually perpendicular to the alignment path and at regular intervals. Sample lines represent the location and orientation of surface cross sections that can be studied through section views. 

Sample lines are created in groups. All sample line groups for an alignment are held in the AeccAlignment.SampleLineGroups collection. The Add method for this collection creates a new empty group, and takes as parameters the name of the group, the layer the group will be drawn to, a style object for how groups of graphs are organized, a style object for the sample lines, and a label style object.
    
    
    ' Get all the styles we will need for our sample line object.
    ' We will use whatever default styles the document contains.
    Dim oGroupPlotStyle As AeccGroupPlotStyle
    Set oGroupPlotStyle = oDocument.GroupPlotStyles.Item(0)
     
    Dim oSampleLineStyle As AeccSampleLineStyle
    Set oSampleLineStyle = oDocument.SampleLineStyles.Item(0)
     
    Dim oSampleLineLabelStyle As AeccLabelStyle
    Set oSampleLineLabelStyle = oDocument _
      .SampleLineLabelStyles.Item(0)
     
    Dim oSampleLineGroups As AeccSampleLineGroups
    Set oSampleLineGroups = oAlignment.SampleLineGroups
     
    ' Create a sample line group using the above styles and drawn
    ' to layer "0".
    Dim sLayerName as String
    sLayerName = "0"
    Dim oSampleLineGroup As AeccSampleLineGroup
    Set oSampleLineGroup = oSampleLineGroups.Add( _
      "Example Sample Line Group", _
      sLayerName, _
      oGroupPlotStyle, _
      oSampleLineStyle, _
      oSampleLineLabelStyle)
