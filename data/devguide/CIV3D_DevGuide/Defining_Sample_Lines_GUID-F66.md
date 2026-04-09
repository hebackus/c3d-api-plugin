<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Sample Lines > Defining Sample Lines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F660F013-A679-41D5-9641-3345665EB6C9.htm -->

# Defining Sample Lines

## Setup

The first step in creating sample lines along an alignment is to specify the surface or surfaces being sampled. This is accomplished by adding surfaces to the AeccSampleLineGroup.SampledSurfaces collection. The AeccSampledSurfaces.AddAllSurfaces method adds one AeccSampledSurface object to the collection for each surface in the document. The AeccSampledSurfaces.Add method takes a specific surface object and an AeccSectionStyle object and returns a reference to the added AeccSampledSurface object. It is important to then set the boolean AeccSampledSurface.Sample property to True.

Note:

If no SampledSurface object added to the AeccSampledSurfaces collection has the Sample property set to True, then no sections will be generated for that sample line.

This sample demonstrates how to add a single surface to a sample line group and how to add all surfaces in the drawing to a sample line group:
    
    
    ' Get the section style we need for our sampled surface
    ' object. We use the default style of the document. 
    Dim oSectionStyle As AeccSectionStyle
    Set oSectionStyle = oDocument.SectionStyles.Item(0)
     
    ' Get the surface object we will be sampling from.
    ' Assume there is a surface with the name "EG".
    Dim oSurface as AeccSurface
    Set oSurface = oDocument.Surfaces.Item("EG")
     
    ' This section demonstrates adding a single surface to
    ' the sample line group. An AeccSampleSurface object is
    ' returned, which needs some properties set.
    Dim oSampledSurface As AeccSampledSurface
    Set oSampledSurface = oSampleLineGroup.SampledSurfaces _
      .Add(oSurface, oSectionStyle)
     
    oSampledSurface.UpdateMode = aeccSectionStateDynamic
    ' We need to set the Sample property of the 
    ' SampledSurface object. Otherwise the sampled surface
    ' will not be used in creating sections. 
    oSampledSurface.Sample = True
     
     
    ' This section demonstrates adding all surfaces in the
    ' document to the sample line group.
    oSampleLineGroup.SampledSurfaces.AddAllSurfaces oSectionStyle
    ' We need to set the Sample property of each 
    ' SampledSurface object. Otherwise the sampled surfaces
    ' will not be used in creating sections. 
    Dim i As Integer
    For i = 0 To oSampleLineGroup.SampledSurfaces.Count - 1
        oSampleLineGroup.SampledSurfaces.Item(i).Sample = True
    Next i
    

At this point you can define sample lines. Sample lines are held in the AeccSampleLineGroup.SampleLines collection. There are three methods to add sample lines to the collection: AeccSampleLines.AddByPolyline, AeccSampleLines.AddByStation, and AeccSampleLines.AddByStationRange.

The AeccSampledSurfaces collection can contain objects other than surfaces to be sampled in section views, such as pipe networks or corridors. These objects can be added from the Autodesk Civil 3D user interface. (Currently you can only add surfaces to the AeccSampledSurfaces collection via the API.)

Accessing these non-surface objects with the AeccSampledSurface.Surface property throws an exception, so you need to use the AeccSampledSurface.AcadEntity property, as in this example, where the second item in the collection is a pipe network:
    
    
    Dim SampledSurfaces As AeccSampledSurfaces
    SampledSurfaces = aeccdb.Sites.Item(0).Alignments.Item(1).SampleLineGroups.Item(0).SampledSurfaces
    Dim s1 As AeccSurface
    Dim e1 As AcadEntity
    Dim s2 As AeccPipeNetwork
    s1 = SampledSurfaces.Item(0).Surface
    e1 = SampledSurfaces.Item(1).AcadEntity ' Surface would throw exception
    MessageBox.Show(e1.ObjectName)
    s2 = e1
    MessageBox.Show(s2.Name)
    

## Adding a Sample Line from a Polyline

AddByPolyline lets you specify the location of a sample line based on an AutoCAD lightweight polyline entity. This gives you great flexibility in designing the sample line. It can consist of many line segments at any orientation, and it does not have to be perpendicular to the alignment or even cross the alignment at all. The AddByPolyline method also lets you delete the polyline entity once the sample line has been created. AddByPolyline returns the AeccSampleLine object created. 
    
    
    Dim oPoly As AcadLWPolyline
    Dim dPoints(0 To 3) As Double
    ' Assume these coordinates are in one of the surfaces 
    ' in the oSampleLineGroup.SampledSurfaces collection.
    dPoints(0) = 4750: dPoints(1) = 4050
    dPoints(2) = 4770: dPoints(3) = 3950
    Set oPoly = ThisDrawing.ModelSpace _
      .AddLightWeightPolyline(dPoints)
     
    ' Now that we have a polyline, we can create a sample line
    ' with those coordinates. Delete the polyline when done.
    Call oSampleLineGroup.SampleLines.AddByPolyline _
      ("Sample Line 01", oPoly, True)
    

## Add a Sample Line at a Station

AddByStation creates a single sample line perpendicular to a particular alignment station. The AddByStation method takes as parameters the name of the sample line, the station the line crosses, and the length of the line to the left and right sides of the alignment. AddByStation returns the AeccSampleLine object created.
    
    
    Dim dSwathWidthLeft As Double
    Dim dSwathWidthRight As Double
    Dim dStation As Double
    dSwathWidthRight = 45.5
    dSwathWidthLeft = 35.5
    dStation = 1100.5
     
    Call oSampleLineGroup.SampleLines.AddByStation( _
      "Sample Line 02", _
      dStation, _
      dSwathWidthLeft, _
      dSwathWidthRight)
    

## Add a Range of Sample Lines

AddByStationRange creates a series of sample lines along the alignment. The characteristics of the sample lines are defined by an object of type AeccStationRange. When first created, the AeccStationRange object properties are set to default values, so be sure to set every property to the values you require. 

Note:

The AeccStationRange.SampleLineStyle property must be set to a valid object or the AddByStationRange method will fail.

The AeccStationRange object is then passed to the AddByStationRange method along with a flag describing how to deal with duplicates. The sample lines are then generated and added to the AeccSampleLineGroup.SampleLines collection. This method has no return value.

This sample adds a series of sample lines along a section of an alignment:
    
    
    ' Specify where the sample lines will be drawn.
    Dim oStationRange As New AeccStationRange
    oStationRange.UseSampleIncrements = True
    oStationRange.SampleAtHighLowPoints = False
    oStationRange.SampleAtHorizontalGeometryPoints = False
    oStationRange.SampleAtSuperelevationCriticalStations = False
    oStationRange.SampleAtRangeEnd = True
    oStationRange.SampleAtRangeStart = True
    oStationRange.StartRangeAtAlignmentStart = False
    oStationRange.EndRangeAtAlignmentEnd = False
    ' Only sample for 1000 units along part of the
    ' alignment.
    oStationRange.StartRange = 10#
    oStationRange.EndRange = 1010#
    ' sample every 200 units along straight lines
    oStationRange.IncrementTangent = 200#
    ' sample every 50 units along curved lines
    oStationRange.IncrementCurve = 50#
    ' sample every 50 units along spiral lines
    oStationRange.IncrementSpiral = 50#
    ' 50 units to either side of the station
    oStationRange.SwathWidthLeft = 50#
    oStationRange.SwathWidthRight = 50#
    oStationRange.SampleLineDefaultDirection = _
      aeccDirectionFromBaseAlignment
    Set oStationRange.SampleLineStyle = oSampleLineStyle
     
    oSampleLineGroup.SampleLines.AddByStationRange _
      "Sample Line 03", _
      aeccSampleLineDuplicateActionOverwrite, _
      oStationRange
