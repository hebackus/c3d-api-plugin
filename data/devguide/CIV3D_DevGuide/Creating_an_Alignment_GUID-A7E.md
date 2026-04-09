<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Basic Alignment Operations > Creating an Alignment -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A7EC290C-9546-411C-A3E1-AB24F250E2AC.htm -->

# Creating an Alignment

Alignments are usually created in existing sites. Each AeccSite object has its own collection of alignments held in an AeccAlignments object in the AeccSite.Alignments property. There is also a collection of alignments that are not associated with a site in the AeccDocument.AlignmentsSiteless property.

## Creating a New Alignment

The AeccAlignments object provides two ways of creating new alignments. The AeccAlignments.Add method takes an alignment name, a layer to draw to, an alignment style object, and an alignment label style object as parameters and returns a new empty alignment. The AeccAlignments.AddFromPolyline method takes the same parameters as well as an AutoCAD polyline entity and flags indicating whether curves should be added between the separate line segments and whether the polyline entity should be erased after the alignment is created. 

This code creates an alignment from a 2D polyline, using existing styles:
    
    
    ' Create an alignment style with default settings.
    Dim oAlignmentStyle as AeccAlignmentStyle
    Set oAlignmentStyle = oDocument.AlignmentStyles _
      .Add("Sample style")
     
    ' Create an alignment label style with default settings.
    Dim oAlignmentLabelStyleSet As AeccAlignmentLabelStyleSet
    Set oAlignmentLabelStyleSet = oAeccDocument.AlignmentLabelStyleSets _
      .Add("Sample label style")
     
    ' Get the collection of all siteless alignments.
    Dim oAlignments as AeccAlignments
    Set oAlignments = oDocument.AlignmentsSiteless
     
    ' Create an empty alignment that draws to layer 0.
    Dim oAlignment as AeccAlignment
    Set oAlignment = oAlignments.Add("Sample Alignment", "0", _
      oAlignmentStyle.Name, oAlignmentLabelStyleSet.Name)
     
     
    ' Create a simple 2D polyline.
    Dim oPoly As AcadLWPolyline
    Dim dPoints(0 To 5) As Double
    dPoints(0) = 0: dPoints(1) = 600
    dPoints(2) = 600: dPoints(3) = 0
    dPoints(4) = 1200: dPoints(5) = 600
    Set oPoly = oDocument.Database.ModelSpace _
      .AddLightWeightPolyline(dPoints)
     
    ' Create an alignment from the polyline object. Draw to
    ' layer 0, erase the polyline when we are done, and
    ' insert curves between line segments.
    Set oAlignment = oAlignments.AddFromPolyline( _
      "Sample Alignment from Polyline", _
      "0", _
      oPoly.ObjectID, _
      oAlignmentStyle.Name, _
      oAlignmentLabelStyleSet.Name, _
      True, _
      True)
    

## Creating an Alignment Offset From Another Alignment

Alignments can also be created based on the layout of existing alignments. The AeccAlignment.Offset method creates a new alignment with a constant offset and adds it to the same parent site as the original alignment. The new alignment has the same name (followed by a number in parenthesis) and the same style as the original, but it does not inherit any station labels, station equations, or design speeds from the original alignment.
    
    
    ' Add an offset alignment 10.5 units to the left of the
    ' original.
    oAlignment.Offset -10.5
