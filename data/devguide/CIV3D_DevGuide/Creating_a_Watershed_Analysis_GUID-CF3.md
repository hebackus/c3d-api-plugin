<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Performing Surface Analysis > Creating a Watershed Analysis -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CF359595-EF4A-4A74-A7DD-C86F8758DE3E.htm -->

# Creating a Watershed Analysis

A watershed analysis predicts how water will flow over and off a surface. The analysis is managed by an object of type AeccSurfaceAnalysisWatershed held in the AeccSurface.SurfaceAnalysis.WatershedAnalysis property. The analysis is created by calling the AeccSurfaceAnalysisWatershed.CalculateWatersheds method. This splits the surface into separate regions, each with its own drain target or targets. The set of all these regions are held in the AeccSurfaceAnalysisWatershed.WatershedRegions collection. 

You have some control over how the regions are split. If the boolean AeccSurfaceAnalysisWatershed.MergeAdjacentBoundaries property is set to True, then regions along the boundary are merged into one region if their boundary points or segments touch. If a depression on the surface has a minimum average depth smaller than the value of the AeccSurfaceAnalysisWatershed.MergeDepression property, then the depression does not become its own region and is combined with the region it drains into. 
    
    
    oSurface.SurfaceAnalysis.WatershedAnalysis _
      .MergeAdjacentBoundaries = True
    oSurface.SurfaceAnalysis.WatershedAnalysis _
      .MergeDepression = 10.65
    

## Types of Watershed Regions

Depending on the nature of the drain target, each watershed region is a different type derived from AeccWatershedRegion. (For more information about watershed region types, see [About Surface Watersheds](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-E021850D-0749-42CC-A49E-6C8BB6CC1DC8>). By checking the Type property of each object in the AeccSurfaceAnalysisWatershed.WatershedRegions collection, you can then determine the specific type of each region. 
    
    
    ' Compute water drainage over the surface.
    oSurface.SurfaceAnalysis.WatershedAnalysis _
      .CalculateWatersheds
     
    ' Extract information from each watershed region. 
    ' Loop through all the regions in the WatershedRegions
    ' collection. For each region, determine its
    ' specific type. Once we cast each region object to this 
    ' specific type, we can learn how water drains over the
    ' surface.
    Dim oWSAnalysis As AeccWatershedRegions
    Set oWSAnalysis = oSurface.SurfaceAnalysis.WatershedAnalysis _
      .WatershedRegions
     
    Dim i as Integer
    For i = 0 To oWSAnalysis.Count - 1
       Select Case (oWSAnalysis.Item(i).Type)
       Case aeccWatershedBoundaryPoint
          Dim oWSPoint As AeccWatershedRegionBoundaryPoint
          Set oWSPoint = oWSAnalysis.Item(i)
     
       Case aeccWatershedBoundarySegment
          Dim oWSSegment As AeccWatershedRegionBoundarySegment
          Set oWSSegment = oWSAnalysis.Item(i)
     
       Case aeccWatershedDepression
          Dim oWSDepression As AeccWatershedRegionDepression
          Set oWSDepression = oWSAnalysis.Item(i)
     
       Case aeccWatershedFlat
          Dim oWSFlat As AeccWatershedRegionFlat
          Set oWSFlat = oWSAnalysis.Item(i)
     
       Case aeccWatershedMultiDrain
          Dim oWSMulti As AeccWatershedRegionMultiRegionDrain
          Set oWSMulti = oWSAnalysis.Item(i)
     
       Case aeccWatershedMultiDrainNotch
          Dim oWSNotch As AeccWatershedRegionMultiRegionDrainNotch
          Set oWSNotch = oWSAnalysis.Item(i)
       Case Else 'aeccWatershedUnknownSink
     
       End Select
    Next i
    

Objects derived from AeccWatershedRegion have other common features. They all have an identification number in the AeccWatershedRegion.Id property. They also have a AeccWatershedRegion.Boundary property, which contains a 2-dimensional array containing the points of a closed polygon enclosing the region. 
    
    
    Dim vBound As Variant
    vBound = oWSAnalysis.Item(i).BoundaryLine
    For j = 0 To UBound(vBound)
       ' Print the X, Y and Z coordinates of a border point.
       Debug.Print vBound(j, 0), vBound(j, 1), vBound(j, 2)
    Next j
    

## Boundary Point Regions

In a region of type AeccWatershedBoundaryPoint, water reaches the boundary of a surface at a single point. The X, Y, and Z coordinates of this point are held in a variant array in the AeccWatershedBoundaryPoint.BoundaryDrainPoint property. 
    
    
    Dim oWSPoint As AeccWatershedRegionBoundaryPoint
    Set oWSPoint = oWSAnalysis.Item(i)
    Dim vDrainPoint As Variant
    vDrainPoint = oWSPoint.BoundaryDrainPoint
    Debug.Print "This region drains to point: " & vDrainPoint(0) _
      & ", " & vDrainPoint(1) & ", " & vDrainPoint(2)
    

## Boundary Segment Regions

Regions of type aeccWatershedBoundarySegment represent areas where water flows out of a surface along a series of line segments. The end points of these line segments are held in a 2-dimensional array of doubles in the aeccWatershedBoundarySegment.BoundaryDrainSegment property. The first dimension of this array represents each point and the second dimension are the X, Y, and Z coordinates of the points. 
    
    
    Dim oWSSegment As AeccWatershedRegionBoundarySegment
    Set oWSBoundarySegment = oWSAnalysis.Item(i)
    Dim vDrainSegments as Variant
    vDrainSegments = oWSBoundarySegment.BoundaryDrainSegment
     
    Dim j as Integer
    Debug.Print "This region drains through the following"
    Debug.Print "line segments:"
    For j = 0 To UBound(vDrainSegments, 1) - 1
       Debug.Print vDrainSegments(j, 0) & ", " _
         & vDrainSegments(j, 1) & ", " _
         & vDrainSegments(j, 2) & "  to  ";
       Debug.Print vDrainSegments(j + 1, 0) & ", " _
         & vDrainSegments(j + 1, 1) _
         & ", " & vDrainSegments(j + 1, 2)
    Next j
    

## Depression Regions

A region of type aeccWatershedDepression represents an area of the surface that water does not normally leave. It is possible for the depression to fill and then drain into other regions. The lowest points on the region edge where this overflow may take place and the regions that the water drains into are kept in the aeccWatershedDepression.Drains collection. 
    
    
    Dim oWSDepression As AeccWatershedRegionDepression
    Set oWSDepression = oWSAnalysis.Item(i)
    Dim oDrains As AeccWatershedDrains
    Set oDrains = oWSDepression.Drains
     
    For j = 0 To oDrains.Count - 1
       ' See what kind of drain targets we have.
       If (UBound(oDrains.Item(j).Targets) = -1) Then
          ' This depression drains outside the surface.
          Debug.Print "Drain through point: " & _ 
            oDrains.Item(j).Location(0) & ", " & _
            oDrains.Item(j).Location(1) & ", " & _
          oDrains.Item(j).Location(2) & _
            " to the surface boundary."
       Else
          ' This depression can drain into other regions.
          Dim lTargets() As Long
          lTargets = oDrains.Item(j).Targets
          sTargets = CStr(lTargets(0))
          Dim k as Integer
          For k = 1 To UBound(lTargets)
             sTargets = sTargets & ", " & CStr(lTargets(k))
          Next k
          Debug.Print "Drain through point: " & _ 
            oDrains.Item(j).Location(0) & ", " & _
            oDrains.Item(j).Location(1) & ", " & _
            oDrains.Item(j).Location(2) & _
            " into the following regions: " & sTargets
       Endif
    Next j
    

## Flat Regions

A flat area that only drains into one region is combined into that region. If a flat surface drains into multiple regions, then it is created as a separate region of type AeccWatershedRegionFlat. The only feature of flat regions is an array of all drain targets. 
    
    
    Dim oWSFlat As AeccWatershedRegionFlat
    Set oWSFlat = oWSAnalysis.Item(i)
     
    varDrainsInto = oWSFlat.DrainsInto
    sTargets = CStr(varDrainsInto(0))
    For k = 1 To UBound(varDrainsInto)
       sTargets = sTargets & ", " & CStr(varDrainsInto(k))
    Next k
    Debug.Print "This region drains into regions " & sTargets
    

## Multiple Drain Regions (Point)

A region of the surface may drain through a point into many different regions. Such regions are represented by an object of type AeccWatershedRegionMultiRegionDrain. These regions have properties containing the point water drains through and a collection of all regions into which water flows. 
    
    
    Dim oWSMulti As AeccWatershedRegionMultiRegionDrain
    Set oWSMulti = oWSAnalysis.Item(i)
     
    ' vDrainPoint is a single point, like BoundaryPoint
    vDrainPoint = oWSMulti.DrainPoint
    ' varDrainsInto is an array of variants, each a region ID.
    varDrainsInto = oWSMulti.DrainsInto
    sTargets = CStr(varDrainsInto(0))
    For k = 1 To UBound(varDrainsInto)
       sTargets = sTargets & ", " & CStr(varDrainsInto(k))
    Next k
     
    Debug.Print "This region drains to point: " & vDrainPoint(0) _
      & ", " & vDrainPoint(1) & ", " & vDrainPoint(2) _
      & " and into the following regions: " & sTargets
    

## Multiple Drain Regions (Notch)

A region can also drain into many other regions through a series of line segments. These regions are represented by an object of type AeccWatershedRegionMultiRegionDrainNotch and they keep both a list of all regions this region drains into and a list of all segments this region drains through. 
    
    
    Dim oWSNotch As AeccWatershedRegionMultiRegionDrainNotch
    Set oWSNotch = oWSAnalysis.Item(i)
    ' vDrainSegments is a 2-dimensional array, like BoundarySegment.
    Dim vDrainSegments As Variant
    vDrainSegments = oWSNotch.DrainSegment
    ' varDrainsInto is an array of region IDs.
    Dim varDrainsInto As Variant
    varDrainsInto = oWSNotch.DrainsInto
     
    sTargets = CStr(varDrainsInto(0))
    For k = 1 To UBound(varDrainsInto)
       sTargets = sTargets & ", " & CStr(varDrainsInto(k))
    Next k
    Debug.Print "This region drains through these segments: "
    For j = 0 To UBound(vDrainSegments, 1) - 1
       Debug.Print vDrainSegments(j, 0) & ", " _
         & vDrainSegments(j, 1) & ", " _
         & vDrainSegments(j, 2) & "  to      ";
       Debug.Print vDrainSegments(j + 1, 0) & ", " _
         & vDrainSegments(j + 1, 1) _
         & ", " & vDrainSegments(j + 1, 2)
    Next j
     
    ' Display each region this drains into.
    Debug.Print "and into the following regions: " & sTargets
