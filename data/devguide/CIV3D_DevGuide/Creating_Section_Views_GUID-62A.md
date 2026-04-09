<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Section Views > Creating Section Views -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-62A68181-648C-4ABC-9DAB-AB36C721355D.htm -->

# Creating Section Views

A section view is a graph of the sections for a single sample. Each sample line contains a collection of section views in its AeccSampleLine.SectionViews property. To create a new section view, use the AeccSectionViews.Add method, which takes as parameters the name of the new section view, the layer to draw to, the location, the style of the view, and an optional data band set. Each section view is automatically constructed to display the sections at that sample line in the center of an appropriately sized graph. As each sample line may have different lengths and represent different surface altitudes, each section view may be different in size or in what units are displayed along each graph axis.

This sample creates a row of section views from all sample lines in a given alignment:
    
    
    Dim i As Integer
    Dim j As Integer
     
    ' Use the first section view style in the document. 
    Dim oSectionViewStyle As AeccSectionViewStyle
    Set oSectionViewStyle = oDocument.SectionViewStyles.Item(0)
     
    ' Specify the starting location of the row of section
    ' views. 
    Dim dX As Double
    Dim dY As Double
    dX = 6000
    dy = 3500
     
    ' We have an alignment with sample lines.  Loop through
    ' all the sample line groups in the alignment.
    For i = 0 To oAlignment.SampleLineGroups.Count - 1
       Dim oSampleLineGroup As AeccSampleLineGroup
       Set oSampleLineGroup = oAlignment.SampleLineGroups.Item(i)
       Dim oSampleLines As AeccSampleLines
       Set oSampleLines = oSampleLineGroup.SampleLines
     
       ' Now loop through all the sample lines in the current
       ' sample line group.  For each sample line, we add a
       ' section view at a unique location with a style and
       ' a data band that we defined earlier.
       Dim dOffsetRight As Double
       dOffsetRight = 0
       For j = 0 To oSampleLines.Count - 1
          Dim oSectionView As AeccSectionView
          dOffsetRight = j * 300
          Dim dOriginPt(0 To 2) As Double
          ' To the right of the surface and the previous
          ' section views.
          dOriginPt(0) = dX + 200 + dOffsetRight
          dOriginPt(1) = dY
          Set oSectionView=oSampleLines.Item(j).SectionViews.Add( _
            "Section View" & CStr(j), _
            "0", _
            dOriginPt, _
            oSectionViewStyle, _
            Nothing) ' "Nothing" means do not display a data band
       Next j
    Next i
